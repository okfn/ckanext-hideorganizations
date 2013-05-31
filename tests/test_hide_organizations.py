import unittest
import nose.tools as tools

import ckan.model
import ckan.logic
import ckan.plugins




class TestHideOrganizations(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        ckan.plugins.load('hideorganizations')
        cls.user = cls._create_user()

    @classmethod
    def teardown_class(cls):
        ckan.plugins.reset()
        ckan.model.repo.rebuild_db()

    def test_dataset_facets_remove_organization(self):
        plugin = self._get_plugin_instance()
        res = plugin.dataset_facets({'organization': 'some-org'}, '')
        assert 'organization' not in res

    def test_group_facets_remove_organization(self):
        plugin = self._get_plugin_instance()
        res = plugin.group_facets({'organization': 'some-org'}, '', '')
        assert 'organization' not in res

    def test_organization_facets_remove_organization(self):
        plugin = self._get_plugin_instance()
        res = plugin.organization_facets({'organization': 'some-org'}, '', '')
        assert 'organization' not in res

    def test_user_is_authorized_to_call_organization_list_for_user(self):
        # This is needed in /dataset/new. This will only work if there're no
        # organizations in CKAN previous to the usage of this extension. If
        # not, they'll be listed in that page (but the user won't be able to
        # do anything with them).
        context = {'user': self.user['name']}
        org = {}
        ckan.logic.get_action('organization_list_for_user')(context, org)

    def test_organization_logic_actions(self):
        actions = [
            'organization_show',
            'organization_list',
            'organization_activity_list',
            'organization_activity_list_html',
            'organization_create',
            'organization_member_create',
            'organization_update',
            'organization_delete'
        ]
        original_group_get = ckan.model.Group.get
        ckan.model.Group.get = staticmethod(lambda id: self._stub_group())
        context = {'user': self.user['name'], 'model': ckan.model}
        org = {'id': 'org-id'}
        for action in actions:
            tools.assert_raises(ckan.logic.NotAuthorized,
                                ckan.logic.get_action(action), context, org)
        ckan.model.Group.get = original_group_get

    def _stub_group(self):
        group = ckan.model.Group()
        group.id = 'some-id'
        return group

    @classmethod
    def _create_user(cls):
        sysadmin = cls._get_sysadmin()
        user_dict = {
            'name': 'billybeane',
            'email': 'billy@beane.org',
            'password': 'b1lly'
        }
        context = {
            'model': ckan.model,
            'session': ckan.model.Session,
            'user': sysadmin['name']
        }
        user = ckan.logic.get_action('user_create')(context, user_dict)
        return user

    @classmethod
    def _get_sysadmin(cls):
        context = {'model': ckan.model, 'ignore_auth': True}
        user_dict = {}
        return ckan.logic.get_action('get_site_user')(context, user_dict)

    def _get_plugin_instance(self):
        interface = ckan.plugins.interfaces.IFacets
        plugins = ckan.plugins.PluginImplementations(interface)
        return [plugin for plugin in plugins
                if plugin.name == 'hideorganizations'][0]
