from setuptools import setup

DESCRIPTION = "A Django Plugin TEXT to SPEECH by Google"

LONG_DESCRIPTION = None

version = '0.1'

try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Framework :: Django',
    'Framework :: Django :: 1.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='django-gtts',
    version=version,
    packages=['django_gtts'],
    author='jiaxin',
    author_email='edison7500@gmail.com',
    url='https://github.com/bit03/django-gtts',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    install_requires=['PySocks>=1.6.8', 'requests>=2.18.1'],
    classifiers=CLASSIFIERS,
    zip_safe=False,
)

__author__ = 'edison7500'
