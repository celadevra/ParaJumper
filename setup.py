""" ParaJumper package setup
"""

from setuptools import setup
import parajumper

setup(
    name="parajumper",
    description="Command line journal/note-taking tool.",
    version=parajumper.__version__,
    entry_points={
        'console_scripts': ['parajumper.cli.main']},
    install_requires=[
        # dev reqs
        # 'pylint',
        # 'pytest',
        'cement == 2.10',
        'clint == 0.5',
        'jieba',
        'pymongo == 3.4',
        'ruamel.yaml'])
