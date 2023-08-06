from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname("__file__"))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'pythcalculus',         
  packages = ['pythcalculus'],   
  version = '0.5',      
  license='GPL 2.0',        
  description = 'Integrate and Differentiate over here!',   
  author = 'Vaishakh Nargund',                  
  author_email = 'vaishakh.nargund1999@gmail.com', 
  long_description=long_description,
  long_description_content_type="text/markdown",     
  url = 'https://github.com/vaish1999/Calculus-in-python',  
  download_url = 'https://github.com/vaish1999/Calculus-in-python/archive/v1.4.tar.gz',   
  keywords = ['calculus', 'python', 'differentiate','integrate','derivative'],   
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
