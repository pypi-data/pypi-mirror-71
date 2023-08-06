import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sample_data", # Replace with your own username
    version="0.0.4",
    author="Joel Horowitz",
    author_email="joelhoro@gmail.com",
    description="A few sample datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelhoro/sample_data",
    packages=setuptools.find_packages(),
    package_data={'sample_data': ['*.csv']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)