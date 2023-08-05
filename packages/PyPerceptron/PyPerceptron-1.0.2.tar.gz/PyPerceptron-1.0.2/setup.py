import os
from setuptools import setup
from os import path


def create_pgk_list(main_pkg: str) -> list:
    """
    :param main_pkg the name of the main package of the python module
    :return a list containing all the sub folder of the main package
    """
    pgks_list = [main_pkg]

    for current_path, folders, files in os.walk('Perceptron'):
        curr_path = '.'.join(current_path.split('\\'))
        for folder in folders:
            if folder != '__pycache__':
                pgks_list.append(curr_path + '.' + folder)

    return pgks_list


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyPerceptron',
    packages=create_pgk_list('Perceptron'),
    version='1.0.2',
    license='MIT',
    description='A python implementation of the build block of the Neural Network, The Perceptron',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Paolo D\'Elia',
    author_email='paolo.delia99@gmail.com',
    url='https://github.com/paolodelia99/Python-Perceptron',
    keywords=['Perceptron', 'Neural Net', 'Machine learning'],  #
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Demo': 'https://github.com/paolodelia99/Python-Perceptron/tree/master/demo',
        'Repo': 'https://github.com/paolodelia99/Python-Perceptron',
    },
)
