# setup.py

import io
from setuptools import setup, find_packages

setup(
    name='dmengine',
    version='0.2.8.dev0',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Distributed Morphology calculator',
    keywords='DM Halle Marantz impoverishment fission linguistics',
    license='MIT',
    url='https://github.com/xflr6/dmengine',
    project_urls={
        'Issue Tracker': 'https://github.com/xflr6/dmengine/issues',
    },
    packages=find_packages(),
    entry_points={'console_scripts': ['dmengine=dmengine.__main__:main']},
    package_data={'dmengine': ['reporting/template.tex']},
    zip_safe=False,
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    install_requires=[
        'oset',
        'PyYAML',
    ],
    extras_require={
        'dev': ['flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=4', 'pytest-cov'],
    },
    long_description=io.open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
