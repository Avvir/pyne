import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynetest",
    version="0.2.7",
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
            "pynetest=pynetest:cli",
        ]
    },
    install_requires=[
        'termcolor',
        'click',
        'click-didyoumean',
        'click-completion'
    ]
)
