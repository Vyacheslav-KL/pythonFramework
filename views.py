from framework.templator import render
from components.models import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 Ok', render('index.html')


class Goods:
    def __call__(self, request):
        logger.log('Product list')
        return '200 Ok', render('goods/goods.html', objects_list=site)


class GoodsCategory:
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


class About:
    def __call__(self, request):
        return '200 Ok', render('about/about.html')


class Contact:
    def __call__(self, request):
        return '200 Ok', render('contact/contact.html')


class Page:
    def __call__(self, request):
        return '200 Ok', render('page/page.html', objects_list=site.categories)


class CreateCategory:

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


class CreateProduct:

    category_id = -1

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

