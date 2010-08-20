from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'selenium>=2.0a5',
    'cherrypy>=3.1.2'
]

setup(name='django-threefour',
    version=version,
    description="A nose plugin that works with Freshen, Django, and Selenium to make BDD testing super fine",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='nose freshen django selenium bdd',
    author='Rob Madole',
    author_email='robmadole@gmail.com',
    url='http://robmadole.com',
    license='BSD',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'nose.plugins.0.10': [
            'threefour = threefour.plugin:ServerPlugin']
    }
)
