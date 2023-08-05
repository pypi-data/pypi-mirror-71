import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timed-functions",  # Replace with your own username
    version="0.1.0",
    description="Decorator to print how long each decorated function takes to complete.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carloshenrique153/timed-functions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.8',
)
