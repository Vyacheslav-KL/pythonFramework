from framework.templator import render
from components.models import Engine, Logger, MapperRegistry
from components.decorators import AppRoute, Debug
from components.cbv import ListView, CreateView
from components.notifier import SmsNotifier, EmailNotifier
from components.unit_of_work import UnitOfWork

site = Engine()
logger = Logger('main')
routes = {}
email = EmailNotifier()
sms = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute(routes=routes, url='/')
class Index(CreateView):

    template = 'index.html'
    logger.log('Index')

    @Debug(name='Index')
    def create_obj(self, data):
        name = site.decode_value(data.get('name'))
        new_obj = site.create_user('client')
        site.clients.append(new_obj)
        schema = {'name': name}
        new_obj.mark_new(schema)
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/goods/')
class Goods:
    @Debug(name='Goods')
    def __call__(self, request):
        logger.log('Product list')
        return '200 Ok', render('goods/goods.html', objects_list=site)


@AppRoute(routes=routes, url='/category-goods/')
class GoodsCategory:
    @Debug(name='category-goods')
    def __call__(self, request):
        logger.log('Product-category list')
        try:
            category = site.find_category(int(request['request_params']['id']))
            return '200 Ok', render('goods/category-goods.html',
                                    objects_list=site,
                                    goods_list=category.goods,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 Ok', render('goods/goods.html', objects_list=site)


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='about')
    def __call__(self, request):
        return '200 Ok', render('about/about.html')


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='contact')
    def __call__(self, request):
        return '200 Ok', render('contact/contact.html')


@AppRoute(routes=routes, url='/page/')
class Page:
    @Debug(name='page')
    def __call__(self, request):
        return '200 Ok', render('page/page.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory(CreateView):
    template = 'page/create-category.html'

    def create_obj(self, data):
        name = site.decode_value(data.get('name'))
        new_category = site.create_category()
        site.categories.append(new_category)
        schema = {'name': name}
        new_category.mark_new(schema)
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-goods/')
class CreateProduct:

    category_id = -1

    @Debug(name='add-goods')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = site.decode_value(data['name'])
            if self.category_id != -1:
                category = site.find_category(int(self.category_id))
                product = site.add_goods(name, category)
                product.observers.append(email)
                product.observers.append(sms)
                site.goods.append(product)
                product.notify()

            return '200 Ok', render('goods/goods.html', objects_list=site)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category(int(self.category_id))
                return '200 Ok', render('page/add-goods.html',
                                        objects_list=site.categories,
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 Ok', 'There are no categories have been added yet'


@AppRoute(routes=routes, url='/users-list/')
class UsersList(ListView):

    template = 'contact/users-list.html'

    def get_queryset(self):
        queryset = MapperRegistry.get_current_mapper('client').all()
        return queryset


@AppRoute(routes=routes, url='/add-user/')
class AddUser(CreateView):

    template = 'contact/add-user.html'

    def create_obj(self, data):
        name = site.decode_value(data['name'])
        new_obj = site.create_user('client')
        site.clients.append(new_obj)
        schema = {'name': name}
        new_obj.mark_new(schema)
        UnitOfWork.get_current().commit()
