from setuptools import setup
# from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "1.0.2"

setup(
    name="almapipy",
    packages=['almapipy'],
    version=VERSION,
    description="Python requests wrapper for the Ex Libris Alma API",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Steve Pelkey",
    author_email="spelkey@ucdavis.edu",
    url='https://github.com/UCDavisLibrary/almapipy',
    install_requires=['requests'],
    python_requires='>=3.0',
    keywords='alma exlibris exlibrisgroup api bibliographic',
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3'
    ]
)
