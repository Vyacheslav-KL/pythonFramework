from jinja2 import FileSystemLoader, Environment


def render(template, folder='templates', static_url='/static/', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    result = env.get_template(template)
    return result.render(**kwargs)
