import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyne",
    version="0.1.11",
    author="Avvir",
    author_email="tira@avvir.io",
    description="A BDD Testing framework for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Avvir/pyne",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        "console_scripts": [
            "pyne=pyne:cli",
        ]
    },
    install_requires=[
        'termcolor',
        'click',
        'click-didyoumean',
        'click-completion'
    ]
)
