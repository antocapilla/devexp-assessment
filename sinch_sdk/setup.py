from setuptools import setup, find_packages

setup(
    name="sinch-sdk",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
            "responses>=0.23.0",
        ]
    }
)