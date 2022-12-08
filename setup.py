from setuptools import find_packages, setup

from netbox.version import __version__

# Load the README.md file
with open(file="README.md", mode="r") as f:
    long_description = f.read()

setup(
    name="netbox",  # define the library name, this is used along wiht `pip install`
    author="Hellboycc",
    author_email="luoyingchuan1210@gmail.com",
    # define the version of the library
    # - MAJOR VERSION 0
    # - MINOR VERSION 0
    # - MAINTENANCE VERSION 1
    version=__version__,
    description="A python simple and flexible CLI tool used to network testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hellboycc/netbox",
    # The packages where I want to build
    packages=find_packages(),
    include_package_data=True,
    # The dependencies the library needs in order to run
    install_requires=["click>=8.1.3", "ping3==4.0.3"],
    # Python version required
    python_requires=">=3.7",
    # Here are the keywords of my library.
    keywords="CLI tool, Network, Software Testing",
    #  Additional classifiers that about the package
    classifiers=[
        # phase of development
        "Development Status :: 3 - Alpha",
        # the audience this library is intended for
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        # Any operating system can use it
        "Operating System :: OS Independent",
        # Specify the version of Python it uses
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        # Library covers
        "Topic :: Software Development :: Libraries",
    ],
    entry_points={"console_scripts": ["netbox-cli = netbox.scripts.command:cli"]},
)
