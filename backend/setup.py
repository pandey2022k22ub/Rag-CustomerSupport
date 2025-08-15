from setuptools import setup, find_packages

setup(
    name="nervespark-backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pymongo",
        "transformers",
        "torch",
        "pytest",
        "flask",
        "flask-cors"
    ]
)
