from setuptools import setup

setup(
    name="livejson",
    py_modules=["livejson"],
    version="1.9.0",
    description="Bind Python objects to JSON files",
    long_description=("An interface to transparently bind Python objects to "
                      "JSON files so that all changes made to the object are "
                      "reflected in the JSON file"),
    keywords="livejson json io development file files live update",
    license="MIT",
    author="Luke Taylor",
    author_email="luke@deentaylor.com",
    url="https://github.com/controversial/livejson/",
)
