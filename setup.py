from distutils.core import setup

setup(
    name='silverpopeye',
    version='0.1.0',
    author='Sidnei Pereira',
    author_email='sidnei.pereira@dp6.com.br',
    packages=['silverpopeye'],
    url='http://pypi.python.org/pypi/silverpopeye/',
    license='LICENSE.txt',
    description='Python client library for Silverpop\'s API.',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests >= 2.0.1",
        "lxml >= 3.2.4",
    ],
)

