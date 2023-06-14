"""
example of a TicketSidebarProvider
"""

from trac.util.html import html as tag
from trac.core import *

from .interface import ITicketSidebarProvider

class SampleTicketSidebarProvider(Component):
    implements(ITicketSidebarProvider)

    def enabled(self, req, ticket):
        return True

    def content(self, req, ticket):
        return tag.b('hello world')
