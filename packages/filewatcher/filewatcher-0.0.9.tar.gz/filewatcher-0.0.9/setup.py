import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="filewatcher", # Replace with your own username
    version="0.0.9",
    author="Krishna",
    author_email="kvrks@outlook.com",
    description="A helper package to monitor files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyberinfy/Tools/blob/master/filewatcher/filewatcher_usage.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
