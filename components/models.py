import quopri
from sqlite3 import connect
from components.notifier import Subject
from components.writer import FileWriter
from components.unit_of_work import DomainObject
from components.mapper import BaseMapper


class User:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.get('name')
        if 'id' in kwargs:
            self.id = kwargs.get('id')


class Admin(User):
    pass


class Client(User, DomainObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UserFactory:
    types = {
        'administrator': Admin,
        'client': Client
    }

    @classmethod
    def create(cls, essence):
        return cls.types[essence]()


class Goods(Subject):

    def __init__(self, name, category):
        super().__init__()
        self.name = name
        self.category = category
        self.category.goods.append(self)


class GoodsFactory:

    @classmethod
    def create(cls, name, category):
        return Goods(name, category)


class Category(DomainObject):

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.get('name')

        if 'id' in kwargs:
            self.id = kwargs.get('id')

        self.goods = []

    def goods_count(self):
        res = len(self.goods)
        return res


class Engine:
    def __init__(self):
        self.admin = []
        self.clients = []
        self.goods = []
        self.categories = []

    @staticmethod
    def create_user(essence):
        return UserFactory.create(essence)

    @staticmethod
    def create_category():
        return Category()

    def find_category(self, item):
        for i in self.categories:
            if i.id == item:
                return i
        raise Exception(f'The category id: {item} does not exist')

    @staticmethod
    def add_goods(essence, name):
        return GoodsFactory.create(essence, name)

    def find_goods(self, name):
        for i in self.goods:
            if i.name == name:
                return i
        return None

    def get_client(self, name):
        for i in self.clients:
            if i.name == name:
                return i

    @staticmethod
    def decode_value(val):
        val = bytes(val.replace('%', '=').replace('+', ' '), 'utf-8')
        return quopri.decodestring(val).decode('utf-8')


class ProductMapper(BaseMapper):
    table_name = 'product'
    model = Goods


class CategoryMapper(BaseMapper):
    table_name = 'categories'
    model = Category

class ClientMapper(BaseMapper):
    table_name = 'clients'
    model = Client


connection = connect('project.sqlite')


class MapperRegistry:
    mappers = {
        'product': ProductMapper,
        'category': CategoryMapper,
        'client': ClientMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Goods):
            return ProductMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Client):
            return ClientMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']
        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        writer = FileWriter(text, self.name)
        writer.writer()

