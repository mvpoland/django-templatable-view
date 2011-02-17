from setuptools import setup, find_packages

setup(
    name = "django-templatable-view",
    version = "0.1",
    url = 'https://github.com/citylive/django-templatable-view',
    license = 'BSD',
    description = "Decorator which takes care of rendering the response in Django views.",
    long_description = open('README','r').read(),
    author = 'Jonathan Slenders, City Live nv',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)

