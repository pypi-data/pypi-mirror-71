# from .pages import *
#  from .settings import *

from ..loader import is_model_registered
from .pages._generic import AGenericPage


__all__ = []

#  Pages

if not is_model_registered('cms', 'GenericPage'):
    class GenericPage(AGenericPage):
        pass

    __all__.append('GenericPage')


from .pages.blog import ABlogIndexPage, ABlogPage, ABlogPageTag


if not is_model_registered('cms', 'BlogPageTag'):
    class BlogPageTag(ABlogPageTag):
        pass

    __all__.append('BlogPageTag')


if not is_model_registered('cms', 'BlogIndexPage'):
    class BlogIndexPage(ABlogIndexPage):
        pass

    __all__.append('BlogIndexPage')


if not is_model_registered('cms', 'BlogPage'):
    class BlogPage(ABlogPage):
        pass

    __all__.append('BlogPage')


from .pages.content import AContentPage


if not is_model_registered('cms', 'ContentPage'):
    class ContentPage(AContentPage):
        pass

    __all__.append('ContentPage')

from .pages.home import AHomePage


if not is_model_registered('cms', 'HomePage'):
    class HomePage(AHomePage):
        pass

    __all__.append('HomePage')

from .pages.document import ADocumentPage

if not is_model_registered('cms', 'DocumentPage'):
    class DocumentPage(ADocumentPage):
        pass

    __all__.append('DocumentPage')
