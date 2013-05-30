import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class HideOrganizationsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')

    def dataset_facets(self, facets_dict, package_type):
        return self._facets(facets_dict)

    def group_facets(self, facets_dict, group_type, package_type):
        return self._facets(facets_dict)

    def organization_facets(self, facets_dict, organization_type,
                            package_type):
        return self._facets(facets_dict)

    def _facets(self, facets_dict):
        if 'organization' in facets_dict:
            del facets_dict['organization']
        return facets_dict
