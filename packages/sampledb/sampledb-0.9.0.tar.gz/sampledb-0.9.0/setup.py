from setuptools import setup, find_packages
import os.path

setup_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(setup_directory, 'README.md')) as readme_file:
    long_description = readme_file.read()

with open(os.path.join(setup_directory, 'requirements.txt')) as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='sampledb',
    version='0.9.0',
    description='A sample and measurement metadata database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sciapp/sampledb',
    author='Florian Rhiem',
    author_email='f.rhiem@fz-juelich.de',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Topic :: Scientific/Engineering',
    ],
    packages=find_packages(exclude=['tests', 'tests.*', 'example_data']),
    install_requires=requirements,
    package_data={
        'sampledb': [
            'static/*/*.*',
            'static/*/*/*.*',
            'static/*/*/*/*.*'
        ],
        'sampledb.logic': [
            'unit_definitions.txt'
        ],
        'sampledb.frontend': [
            'templates/*/*.*',
            'templates/*/*/*.*',
            'templates/*/*/*/*.*'
        ]
    }
)
