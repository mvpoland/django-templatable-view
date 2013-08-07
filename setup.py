import datetime
import os
from setuptools import setup, find_packages
import subprocess

def get_git_version():
    git_dir = os.path.abspath(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '.git'
        )
    )
    try:
        # Python 2.7 has subprocess.check_output
        # 2.6 needs this longer version
        git_info = subprocess.Popen(['git', '--git-dir=%s' % git_dir, 'log', '--pretty=%ct %h', '-1'], stdout=subprocess.PIPE).communicate()[0].split()
        git_time = datetime.datetime.fromtimestamp(float(git_info[0]))
    except Exception:
        git_time = datetime.datetime.now()
        git_info = ('', '0000000')
    return git_time.strftime('%Y.%m.%d') + '.' + git_info[1]

__version__ = get_git_version()

setup(
    name = "django-templatable-view",
    version = __version__,
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

