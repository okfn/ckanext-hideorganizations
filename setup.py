from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-hideorganizations',
	version=version,
	description="Hide organizations",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Vitor Baptista',
	author_email='vitor@vitorbaptista.com',
	url='',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.hideorganizations'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
        hideorganizations=ckanext.hideorganizations.plugin:HideOrganizationsPlugin
	""",
)
