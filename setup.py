import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyble",
    version="0.1.0",
    author="",
    author_email="",
    description="Nice little wrapper library that calls dbus to use BLE features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hulloanson/pyble",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: GNU Linux",
    ],
    # TODO: find out a better way to install dependencies
    # install_requires=[
    #     'dbus-python',
    #     'gobject'
    # ]
)
