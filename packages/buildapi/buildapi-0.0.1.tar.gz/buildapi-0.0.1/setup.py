from setuptools import setup, find_packages

setup(
    name = 'buildapi',
    version = '0.0.1',
    keywords='buildapi',
    description = 'a library for build http api',
    license = 'Mozilla Public License 2.0',
    url = 'https://github.com/snbck/buildApi',
    author = 'snbck',
    author_email = 'snbckcode@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)