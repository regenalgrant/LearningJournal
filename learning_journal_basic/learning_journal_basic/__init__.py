from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.route')
    config.add_static_view(name='static', path='learning_journal_basic:static')
    config.scan()
    return config.make_wsgi_app()
