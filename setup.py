from setuptools import setup

setup(
    name="git-trend",
    version='0.1',
    py_modules=['get_trending_items'],
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