from views import Index, About, Goods, Contact, Page, CreateCategory, \
    CreateProduct, GoodsCategory


routes = {
    '/': Index(),
    '/goods/': Goods(),
    '/about/': About(),
    '/contact/': Contact(),
    '/page/': Page(),
    '/create-category/': CreateCategory(),
    '/add-goods/': CreateProduct(),
    '/category-goods/': GoodsCategory(),
}
