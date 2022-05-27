from framework.templator import render
from components.models import Engine, Logger
from components.decorators import AppRoute, Debug

site = Engine()
logger = Logger('main')
routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 Ok', render('index.html')


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
class CreateCategory:
    @Debug(name='create-category')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = site.decode_value(data['name'])
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            return '200 Ok', render('goods/goods.html',
                                    objects_list=site)

        else:
            return '200 Ok', render('page/create-category.html',
                                    objects_list=site.categories)


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
                site.goods.append(product)

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

