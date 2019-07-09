import setuptools

long_description = """xc is a simple calculator meant to be used entirely from the command-line. It automatically displays results in both decimal and hexidecimal. It is focused on convenience and ease of use."""

__version__ = '0.8'

setuptools.setup(
    name='xc',
    version=__version__,
    author='Dustin Long',
    author_email='me@dustmop.io',
    description='xc is a simple command-line calculator with hex conversions',
    long_description=long_description,
    url='https://github.com/dustmop/xc',
    scripts=['bin/xc'],
    packages=[''],
    license='GPL3',
    keywords='hex hexidecimal calc calculator command-line commandline',
)
