from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from quickstart.serializers import UsersSerializer, LoginSerializer, ItemsSerializer, CartSerializer, TokenSerializer
from .models import Items, Cart
from quickstart.tasks import create_new_item, send_ok_email
from drf_yasg.utils import swagger_auto_schema

class NeedLogin(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You need to login'
    default_code = 'not_authenticated'


class IsLogin(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            print(request.user)
            return True
        raise NeedLogin()


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]


class UserLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(query_serializer=UsersSerializer,
                         responses={200: UsersSerializer(many=True)})
    def post(self, request, format=None):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])

        if user:
            return Response('success', status=status.HTTP_200_OK)
        else:
            return Response('error', status=status.HTTP_400_BAD_REQUEST)


class ItemsView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ItemsSerializer

    @swagger_auto_schema(query_serializer=ItemsSerializer,
                         responses={200: ItemsSerializer(many=True)})
    def get(self, request):
        # name and price gets from url (?name=kavo&&price=None)
        name = request.GET.get('name', None)
        print(request.user, request.auth)
        description = request.GET.get('description', None)
        if name and description:
            # Возвращаем отфильтрованые записи
            queryset = Items.objects.filter(
                name__contains=name,
                description__contains=description)
            serializer = self.serializer_class(data=queryset, many=True)
            serializer.is_valid()
            return Response(serializer.data)
        elif name:
            queryset = Items.objects.filter(name__contains=name)
            serializer = self.serializer_class(data=queryset, many=True)
            serializer.is_valid()
            return Response(serializer.data)
        elif description:
            queryset = Items.objects.filter(description__contains=description)
            serializer = self.serializer_class(data=queryset, many=True)
            serializer.is_valid()
            return Response(serializer.data)
        else:
            queryset = Items.objects.all()
            serializer = ItemsSerializer(queryset, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(query_serializer=ItemsSerializer,
                         responses={200: ItemsSerializer(many=True)})
    def post(self, request):
        # Создать items
        serializer = ItemsSerializer(data=request.data)
        create_new_item.delay()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailView(APIView):
    # ради интереса сделал ссылки на разные итемы, с возможностью удалить их
    # по урлу типа "items/1"
    permission_classes = [AllowAny]
    serializer_class = ItemsSerializer

    def get(self, request, pk):
        item = get_object_or_404(Items, pk=pk)
        serializer = ItemsSerializer(item)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        item = get_object_or_404(Items, pk=pk)
        item.delete()
        return Response(f"item '{item.name}' was deleted")

    def put(self, request, pk):
        item = get_object_or_404(Items, pk=pk)
        serializer = ItemsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CartSerializer

    def get(self, request):
        ip = request.META.get('REMOTE_ADDR')
        user = {'user': f"{ip}"}

        return Response(user)

    @swagger_auto_schema(query_serializer=CartSerializer,
                         responses={200: CartSerializer(many=True)})
    def post(self, request):
        # Принимал на вход item_id
        # Создать карзину
        #user_id = get_object_or_404(User, username=request.user)
        token = get_object_or_404(Token, key=request.auth)
        print(token)
        user = get_object_or_404(User, id=token.user_id)
        mail = user.email
        print(mail)
        #request.data['user'] = token.user_id
        data = {'user': token.user_id, 'item': [int(i) for i in request.data['item'] if i.isdigit()]}
        print(data)
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            send_ok_email.delay(mail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenCheck(APIView):
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    def get(self, request):
        # Список токенов
        tokens = Token.objects.all()
        serializer = TokenSerializer(tokens, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Создать items
        serializer = ItemsSerializer(data=request.data)
        create_new_item.delay()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




