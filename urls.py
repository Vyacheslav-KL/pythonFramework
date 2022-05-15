from views import Index, About, Goods, Contact, Page


routes = {
    '/': Index(),
    '/goods/': Goods(),
    '/about/': About(),
    '/contact/': Contact(),
    '/page/': Page(),
}
