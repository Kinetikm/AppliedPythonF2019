import os
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


# read requirements
fname = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(fname) as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name='registration',
    version=1,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'registration = src.run:main'
        ],
    },
    author='Terebonka',
    description='Registration Service',
    url='https://github.com/Kinetikm/AppliedPythonF2019',
    license="MIT",
)
