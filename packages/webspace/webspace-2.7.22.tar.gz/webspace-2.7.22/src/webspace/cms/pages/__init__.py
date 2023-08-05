from ...loader import is_model_registered
from .document import DocumentPage as ADocumentPage

__all__ = []


if not is_model_registered('cms', 'DocumentPage'):
    class DocumentPage(ADocumentPage):
        pass
    __all__.append('DocumentPage')


# from .content import ContentPage
# from .home import HomePage
# from .blog import BlogPageTag, BlogIndexPage, BlogPage
