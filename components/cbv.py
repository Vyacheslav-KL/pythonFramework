from framework.templator import render


class TemplateView:
    template = 'template.html'

    def render_template(self):
        return '200 Ok', render(self.template, **{})

    def __call__(self, request):
        return self.render_template()


class ListView(TemplateView):
    queryset = []

    def render_template(self):
        context_data = {'objects_list': self.queryset}
        print(context_data)
        return '200 Ok', render(self.template, **context_data)


class CreateView(TemplateView):

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            self.create_obj(request['data'])
            return self.render_template()
        else:
            return super().__call__(request)
