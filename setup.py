from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name="krpsim",
    version="0.0.1",
    author="John Afaghpour",
    author_email="johnafaghpour@gmail.com",
    description="Program that will optimize the performance of a process graph, with resource constraints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jafaghpo/Krpsim",
    package_dir={'': 'src'},
    license=license,
    packages=find_packages('src', exclude=('tests', 'docs')),
    python_requires=">=3.9",
)