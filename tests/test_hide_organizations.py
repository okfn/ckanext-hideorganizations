import unittest

import ckan.plugins


class TestHideOrganizations(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        ckan.plugins.load('hideorganizations')

    @classmethod
    def teardown_class(cls):
        ckan.plugins.reset()

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

    def _get_plugin_instance(self):
        interface = ckan.plugins.interfaces.IFacets
        plugins = ckan.plugins.PluginImplementations(interface)
        return [plugin for plugin in plugins
                if plugin.name == 'hideorganizations'][0]
