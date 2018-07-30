import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pin_py",
    version="0.0.5",
    author="Hassan Alvi",
    author_email="hassan.awan@d4interactive.io",
    description="Python wrapper for pinterest API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d4interactive/pinterest-api",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)