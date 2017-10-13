from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-partial-date-field',
    version='1.0.0',

    description='Django custom model field for partial dates with the form YYYY, YYYY-MM, YYYY-MM-DD',
    long_description=long_description,

    url='https://github.com/ktowen/django-partial-date-field',

    author='ktowen',
    author_email='towenpa@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    keywords=['fields', 'django', 'dates', 'partial'],

    packages=['partial_date'],
)
