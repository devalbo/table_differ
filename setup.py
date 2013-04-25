from distutils.core import setup

setup(
    name='TableDiffer',
    version='0.1dev',
    packages=['table_differ',],
    license='',
    long_description=open('README.md').read(),
    requires=['Flask==0.9',
              'Jinja2==2.6',
              'Werkzeug==0.8.3',
              'argparse==1.2.1',
              'distribute==0.6.31',
              'wsgiref==0.1.2',
              ],
    )
