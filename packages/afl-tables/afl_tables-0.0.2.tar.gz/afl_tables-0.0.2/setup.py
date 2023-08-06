from setuptools import setup, find_packages

setup(
    name='afl_tables',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'html5lib',
        'pytz'
    ],
    author='Michael Milton',
    author_email='michael.r.milton@gmail.com',
    license='GPLv3',
    entry_points={
        'console_scripts': [
            'afltables = afl_tables.cli:main',
        ]
    },
    extras_require={
        "dev": [
            "pytest",
            "sphinx",
            "recommonmark"
        ],
    }
)
