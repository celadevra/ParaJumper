""" ParaJumper package setup
"""

from setuptools import setup
import parajumper

setup(
    name="parajumper",
    description="Command line journal/note-taking tool.",
    version=parajumper.__version__,
    packages=['parajumper', 'parajumper/cli'],
    entry_points={
        'console_scripts': ['parajumper = parajumper.cli.main:main']},
    install_requires=[
        # dev reqs
        # 'pylint',
        # 'pytest',
        'clint >= 0.5',
        'jieba',
        'pymongo >= 3.4',
        'ruamel.yaml'])
