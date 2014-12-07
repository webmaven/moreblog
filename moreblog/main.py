import os
import inspect
import morepath

from morepath import redirect
import sqlalchemy
from more.transaction import transaction_app
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register
from werkzeug.serving import run_simple

from . import model

Session = scoped_session(sessionmaker())
register(Session)

class ChameleonApp(morepath.App):

    @morepath.reify
    def chameleon_template_paths(self):
        paths = self.registry.settings.chameleon.search_paths
        def expand_paths(paths):
            for ix, item in enumerate(paths):
                # if the returned item is
                if inspect.isclass(item):
                    for path in item().chameleon_template_paths:
                        yield path
                elif not item.startswith('/'):
                    yield os.path.join(
                        os.path.dirname(inspect.getfile(self.__class__)), item)
                else:
                    yield item

        return list(
            expand_paths(self.registry.settings.chameleon.search_paths))

    @morepath.reify
    def chameleon_templates(self):
        """ Returns an instanace of the chameleon.PageTemplateLoader with
        the template paths set to `chameleon_template_paths`

        """

        if self.registry.settings.chameleon.auto_reload:
            # this will result in a warning from chameleon at the moment:
            # https://github.com/malthe/chameleon/issues/183
            os.environ['CHAMELEON_RELOAD'] = 'true'

        # Only import after setting the environment variable, or it won't
        # be recognized.
        import chameleon
        return chameleon.PageTemplateLoader(self.chameleon_template_paths)

@ChameleonApp.setting(section="chameleon", name="search_paths")
def get_search_paths():
    """ Returns the chameleon search paths for the app. """
    #raise NotImplementedError
    return ['templates']

@ChameleonApp.setting(section="chameleon", name="auto_reload")
def get_debug():
    """ Returns True if the template files should be automatically reloaded.

    """

    # TODO configure this for deployment
    return True


def render_chameleon(content, request):
    """ Renders the content with a chameleon template.
    The content is a dictionary of template variables used in the template.

    """
    template = request.app.chameleon_templates[content.pop('template')]
    rendered = template(**content)

    return morepath.request.Response(rendered, content_type='text/html')

@ChameleonApp.directive('chameleon')
class ChameleonDirective(morepath.directive.ViewDirective):
    """ Chameleon template view directive. Use like a morepath view::

    @MyApp.chameleon(model=Root, path='')
    def root(self, request, form=None):
        return {
            'template': 'blogpost.pt',
            'title': 'My Blog Post'
        }

    """
    def __init__(self, app, model, render=None, permission=None,
                 internal=False, **predicates):
        """ Register Chameleon view. """

        render = render or render_chameleon
        super(ChameleonDirective, self).__init__(
            app, model, render, permission, internal, **predicates)

    def group_key(self):
        return morepath.directive.ViewDirective

class App(ChameleonApp):
    pass

def main():
    engine = sqlalchemy.create_engine('sqlite:///morepath_sqlalchemy.db')
    Session.configure(bind=engine)
    model.Base.metadata.create_all(engine)
    model.Base.metadata.bind = engine

    morepath.autosetup()
    run_simple('localhost', 8080, App(), use_reloader=True)
