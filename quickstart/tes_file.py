



class Base:
    
    name = None
    age = None
    city = None
    
    def _post(self):
        print('hello')
    
    def __get(self, name):
        print(name)
        
        
class BaseTest(Base):
    
    name = 'Max'
    age = 20
    city = 'Tambov'
    
    def get(self, name):
        print(f'your name is {name}')
    
    
    
test = BaseTest()
test_2 = Base()
#test_2.get('Sasha_2')
test.get('Sasha')
test._post()
test._Base__get('Sasha')