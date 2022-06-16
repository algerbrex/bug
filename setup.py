from distutils.core import setup
from setuptools import find_packages


DESCRIPTION = '''\
Bug is a simple, toy programming language'''


setup(
    name='Schemey',
    description=DESCRIPTION,
    author="Christian Dean",
    version='0.1',
    packages=find_packages(),
    license='MIT',
    entry_points={
        'console_scripts': [
            'bug = bug.main:main',
        ],
    },
)
