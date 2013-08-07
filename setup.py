from setuptools import setup, find_packages
import templatable_view

setup(
    name = "django-templatable-view",
    version = templatable_view.__version__,
    url = 'https://github.com/citylive/django-templatable-view',
    license = 'BSD',
    description = "Decorator which takes care of rendering the response in Django views.",
    long_description = open('README.rst','r').read(),
    author = 'Jonathan Slenders, City Live nv',
    packages = find_packages('templatable_view'),
    package_dir = {'': 'templatable_view'},
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)

