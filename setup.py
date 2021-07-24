import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open('version', 'r') as f:
    version = f.read()


setuptools.setup(
    name='mangareader',
    version=version,
    scripts=['manga'],
    author="Duncan Sommerville",
    author_email="duncan.sommerville@gmail.com",
    description="Command line interface for searching, downloading, and reading manga",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=["mangareader"],
    package_dir={"": "src"},
    install_requires=[
        "click==7.1.1",
        "requests==2.23.0",
        "Whoosh==2.7.4",
        "beautifulsoup4==4.9.0",
        "lxml==4.5.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    test_suite="tests"
)
