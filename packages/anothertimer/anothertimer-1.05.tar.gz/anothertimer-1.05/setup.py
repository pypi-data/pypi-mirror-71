from distutils.core import setup


with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
  name = 'anothertimer',
  packages = ['anothertimer'],
  version = '1.05',     
  license='MIT',
  description = 'Literally another code timer (with fancy plotting)',
  long_description = long_description,
  author = 'Dang Pham',
  author_email = 'dang.c.pham@hotmail.com',
  url = 'https://github.com/dangcpham/anothertimer',
  download_url= 'https://github.com/dangcpham/anothertimer/archive/v1.05.tar.gz',
  keywords = ['time', 'timer', 'timing'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
