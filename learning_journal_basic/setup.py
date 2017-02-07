import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'pyramid_jinja2',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'faker',
    'ipython',
    'pyramid-ipython'
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    'pytest-watch',
    'tox'
    ]

development_extra = [
    'ipython',
    'pyramid_ipython'
]
setup(name='learning_journal_basic',
      version='0.0',
      description='learning_journal_basic',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='REGENAL GRANT',
      author_email='regenal@gmail.com',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
          'developer': development_extra,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = learning_journal_basic:main
      [console_scripts]
      initialize_db = learning_journal_basic.scripts.initializedb:main""",
      )
