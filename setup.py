import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open('version', 'r') as f:
    version = f.read()


setuptools.setup(
    name='manga-reader-cli',
    version=version,
    scripts=['manga'],
    author="Duncan Sommerville",
    author_email="duncan.sommerville@gmail.com",
    description="Command line interface for searching, downloading, and reading manga",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    test_suite="reader/test"
)
