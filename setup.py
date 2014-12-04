from setuptools import setup, find_packages

setup(name='moreblog',
      packages=find_packages(),
      install_requires=[
        'setuptools',
        'morepath',
        'transaction',
        'more.transaction',
        'zope.sqlalchemy >= 0.7.4',
        'sqlalchemy >= 0.9',
        ],
      entry_points={
         'console_scripts': [
          'moreblog-start = moreblog.main:main'
          ]
      })
