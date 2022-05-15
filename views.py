from framework.templator import render


class Index:
    def __call__(self):
        return '200 Ok', render('index.html')


class Goods:
    def __call__(self):
        return '200 Ok', render('goods.html')


class About:
    def __call__(self):
        return '200 Ok', render('about.html')


class Contact:
    def __call__(self):
        return '200 Ok', render('contact.html')


class Page:
    def __call__(self):
        return '200 Ok', render('page.html')
