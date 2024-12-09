from setuptools import setup, find_packages

setup(
    name="sinch_sdk",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1'
        'flask'
    ],
)