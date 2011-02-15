import re

from lxml import etree

from .search import SearchManager
from .users import Users
from .resources import Project
from .tags import Tags
from .schema import datatypes, datatype_attributes, resources_singular
from .uriutil import join_uri

class GlobalManager(object):
    def __init__(self, interface):
        self._intf = interface

        self.search = SearchManager(self._intf)
        self.users = Users(self._intf)
        self.tags = Tags(self._intf)
        self.schemas = SchemaManager(self._intf)

    def set_callback(self, func=None):
        """ Defines a callback to execute when collections of resources are 
            accessed.

            Parameters
            ----------
            func: callable
                A callable that takes the current collection object as first 
                argument and the current element object as second argument.

            Examples
            --------
            >>> def notify(cobj, eobj):
            >>>    print eobj._uri
            >>> interface.manage.set_callback(notify)
        """
        self._intf.callback = func

    def project(self, project_id):
        return ProjectManager(project_id, self._intf)


class ProjectManager(object):
    def __init__(self, project_id, interface):
        self._intf = interface
        project = Project('/REST/projects/%s'%project_id, self._intf)

        self.prearchive_code = project.prearchive_code
        self.set_prearchive_code = project.set_prearchive_code
        self.quarantine_code = project.quarantine_code
        self.set_quarantine_code = project.set_quarantine_code
        self.current_arc = project.current_arc
        self.set_subfolder_in_current_arc = \
            project.set_subfolder_in_current_arc
        self.accessibility = project.accessibility
        self.users = project.users
        self.owners = project.owners
        self.members = project.members
        self.collaborators = project.collaborators
        self.user_role = project.user_role
        self.add_user = project.add_user
        self.remove_user = project.remove_user


class SchemaManager(object):
    def __init__(self, interface):
        self._intf = interface
        self._trees = {}

    def _init(self):
        if self._trees == {}:

            for entry in self._intf.cache.entries():
                if entry.endswith('.xsd'):
                    url  = re.findall('schemas/.*', entry)[0]
                    self._trees[url.split('/')[-1]] = \
                        etree.fromstring(self._intf._exec(url))

    def __call__(self):
        self._init()
        return self._trees.keys()

    def add(self, url):
        """ Loads an additional schema.

            Parameters
            ----------
            url: str
                url of the schema relative to the server.
                e.g. for http://central.xnat.org/schemas/xnat/xnat.xsd
                     give schemas/xnat/xnat.xsd
        """
        self._init()
        
        if not re.match('/?schemas/.*/.*\.xsd', url):
            if not 'schemas' in url and re.match('/?\w+/\w+[.]xsd', url):
                url = join_uri('/schemas', url)

            elif not re.match('^[^/].xsd', url):
                url = '/schemas/%s/%s'%(url.split('.xsd')[0], url)
            else:
                raise NotImplementedError
                
        self._trees[url.split('/')[-1]] = \
            etree.fromstring(self._intf._exec(url))

    def remove(self, name):
        if self._trees.has_key(name):
            del self._trees[name]

#    def docs(self):
#        self._init()
#        return self._trees.values()


#class LocalLayout(object):
#    def __init__(self, interface):
#        self._intf = interface

#        self.root_dir = None
#        self.templates = 

#            ('/projects/%(project)s/subjects/%(subject)s'
#             '/experiments/%(experiment)s/projects/%(project)s/'
#        self._attrs = {}


#    def set_root(self, root_dir):
#        self.root_dir = root_dir

#    def set_attr(self, key, method):
#        if key not in resources_singular:
#            raise Exception("Key error '%s': must be one of %s"%key, resources_singular)

#        self._attrs[key] = method

#    def transform(self, uri):
#        obj = self._intf.select(uri)
#        attrs = {}

#        for key in self._attrs.keys()
#            attrs[key] = getattr(obj, self._attrs[key])






