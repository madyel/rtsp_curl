from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='rtsp_curl',
      version='0.6',
      description='Convert rtsp.c to rtsp_curl.py',
      url='https://github.com/madyel/rtsp_curl',
      author='MaDyEl',
      author_email='madyel@countermail.com',
      license='MIT',
      packages=['madyel'],
      install_requires=['scanf>=1.5.2',
                        'pycurl==7.43.0.2'],
      long_description=long_description,
      long_description_content_type='text/markdown'
      )