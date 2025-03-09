from setuptools import setup, find_packages

setup(
    name="s2s_back",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            's2s_back=s2s_back.main:main',
        ],
    },
)
