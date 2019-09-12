from setuptools import setup
#from distutils.core import setup
try:
    from pypandoc import convert

    def read_md(f): return convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")

    def read_md(f): return open(f, 'r').read()


VERSION = "1.0.1"

setup(
    name="almapipy",
    packages=['almapipy'],
    version=VERSION,
    description="Python requests wrapper for the Ex Libris Alma API",
    license='MIT',
    long_description=read_md('README.md'),
    author="Steve Pelkey",
    author_email="spelkey@ucdavis.edu",
    url='https://github.com/UCDavisLibrary/almapipy',
    install_requires=['requests'],
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

        'Programming Language :: Python :: 3.6'
    ]
)
