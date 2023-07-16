import pathlib
from setuptools import setup, find_packages

setup(
    name='dmengine',
    version='0.3.2.dev0',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Distributed Morphology calculator',
    keywords='DM Halle Marantz impoverishment fission linguistics',
    license='MIT',
    url='https://github.com/xflr6/dmengine',
    project_urls={
        'Issue Tracker': 'https://github.com/xflr6/dmengine/issues',
        'CI': 'https://github.com/xflr6/dmengine/actions',
    },
    packages=find_packages(),
    entry_points={'console_scripts': ['dmengine=dmengine.__main__:main']},
    package_data={'dmengine': ['reporting/template.tex']},
    zip_safe=False,
    platforms='any',
    python_requires='>=3.8',
    install_requires=['PyYAML'],
    extras_require={
        'dev': ['flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=7', 'pytest-cov'],
    },
    long_description=pathlib.Path('README.rst').read_text(encoding='utf-8'),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
