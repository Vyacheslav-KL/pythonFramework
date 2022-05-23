import quopri


class User:
    pass


class Admin(User):
    pass


class Client(User):
    pass


class UserFactory:
    types = {
        'administrator': Admin,
        'client': Client
    }

    @classmethod
    def create(cls, essence):
        return cls.types[essence]()


class Goods:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.goods.append(self)


class GoodsFactory:

    @classmethod
    def create(cls, name, category):
        return Goods(name, category)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.goods = []

    def goods_count(self):
        res = len(self.goods)
        if self.category:
            res += self.category.goods_count()
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
    def create_category(name, category=None):
        return Category(name, category)

    def find_category(self, item):
        for i in self.categories:
            if i.id == item:
                return i
        raise Exception(f'The category id: {item} does not exist')

    @staticmethod
    def add_goods(name, category):
        return GoodsFactory.create(name, category)

    def find_goods(self, name):
        for i in self.goods:
            if i.name == name:
                return i
        return None

    @staticmethod
    def decode_value(val):
        val = bytes(val.replace('%', '=').replace('+', ' '), 'utf-8')
        return quopri.decodestring(val).decode('utf-8')


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

    @staticmethod
    def log(text):
        print('log:', text)
