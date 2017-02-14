# _*_ coding: utf-8 _*_
from distutils.core import setup
from setuptools import setup

setup(
    name='git-trend',
    version='0.1.2.1',
    author='Manoj Karthick',
    author_email='manojkarthick@ymail.com',
    url='https://github.com/manojkarthick/git-trend',
    license='MIT License',
    description='A Python CLI tool for getting the trending github repositories and developers',
    py_modules=['get_trending_items'],
    keywords = ['github', 'trending', 'repositories','developers','languages'], # arbitrary keywords
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'termcolor',
        'bs4',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        git-trend=get_trending_items:cli
    ''',
)