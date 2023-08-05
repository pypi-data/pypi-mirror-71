from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='probability_distributions_12b',
      version='0.2',
      description='Gaussian and Binomial distributions',
      packages=['probability_distributions_12b'],
      author_email='bucsab12@gmail.com',
      # other arguments omitted
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
