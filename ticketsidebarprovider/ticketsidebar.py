"""
TicketSidebarProvider
a plugin for Trac to provide content alongside the ticket
http://trac.edgewall.org/wiki/TracTicketsCustomFields
"""

from trac.util.html import html as tag
from pkg_resources import resource_filename

from trac.config import Option
from trac.core import *
from trac.web.api import IRequestFilter
from trac.web.chrome import add_script, add_script_data, add_stylesheet
from trac.web.chrome import ITemplateProvider

from ticketsidebarprovider.interface import ITicketSidebarProvider

from .jtransformer import JTransformer


class TicketSidebarProvider(Component):

    implements(IRequestFilter, ITemplateProvider)

    providers = ExtensionPoint(ITicketSidebarProvider)

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):

        if template != 'ticket.html':
            return template, data, content_type

        ticket = data['ticket']
        filter_lst = []
        for provider in self.providers: # TODO : sorting
            if provider.enabled(req, ticket):
                filter = JTransformer('div#content')
                filter_lst.append(
                    filter.after(str(tag.div(provider.content(req, ticket),
                                             **{'class': "sidebar" })))
                )
        add_stylesheet(req, 'common/css/ticket-sidebar.css')
        add_script_data(req, {'tsbp_filter': filter_lst})
        add_script(req, 'common/js/ct_jtransform.js')
        return template, data, content_type

    def get_htdocs_dirs(self):
        """Return a list of directories with static resources (such as style
        sheets, images, etc.)

        Each item in the list must be a `(prefix, abspath)` tuple. The
        `prefix` part defines the path in the URL that requests to these
        resources are prefixed with.
        
        The `abspath` is the absolute path to the directory containing the
        resources on the local file system.
        """
        return [('common', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        """Return a list of directories containing the provided template
        files.
        """
        return []
