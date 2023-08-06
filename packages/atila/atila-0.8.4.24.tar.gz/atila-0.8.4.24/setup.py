"""
Hans Roh 2015 -- http://osp.skitai.com
License: BSD
"""
import re
import sys
import os
import shutil, glob
import codecs
from warnings import warn
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

with open('atila/__init__.py', 'r') as fd:
	version = re.search(r'^__version__\s*=\s*"(.*?)"',fd.read(), re.M).group(1)

classifiers = [
  'License :: OSI Approved :: MIT License',
  'Development Status :: 4 - Beta',
	'Topic :: Internet :: WWW/HTTP :: WSGI',
	'Environment :: Console',
	'Topic :: Internet',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Intended Audience :: Developers',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
	'Programming Language :: Python :: Implementation :: CPython',
	'Programming Language :: Python :: Implementation :: PyPy'
]

packages = [
	'atila',
	'atila.app',
	'atila.patches'
]

package_dir = {'atila': 'atila'}
package_data = {}

install_requires = [
	"skitai>=0.34.2",
	"css_html_js_minify; python_version>='3.6'"
]

with codecs.open ('README.rst', 'r', encoding='utf-8') as f:
	long_description = f.read()

setup (
	name='atila',
	version=version,
	description='Atila Framework',
	long_description=long_description,
	url = 'https://gitlab.com/hansroh/atila',
	author='Hans Roh',
	author_email='hansroh@gmail.com',
	packages=packages,
	package_dir=package_dir,
	package_data = package_data,
	entry_points = {},
	license='MIT',
	platforms = ["posix", "nt"],
	download_url = "https://pypi.python.org/pypi/atila",
	install_requires = install_requires,
	classifiers=classifiers
)
