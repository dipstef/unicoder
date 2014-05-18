from distutils.core import setup

VERSION = '0.1'

desc = """Handle unicode conversion and normalization.
On decoding errors uses auxiliary library (beautiful soup, chardet) to guess the encoding"""

name = 'unicoder'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description='Misc date utilities functions',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=[name],
      platforms=['Any'],
      long_description=desc,
      requires=['BeautifulSoup4', 'chardet']
)