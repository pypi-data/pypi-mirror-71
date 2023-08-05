import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="var-io", # Replace with your own username
    version="0.1.8",
    author="karond",
    author_email="dingyaohui.g@outlook.com",
    description="Save your variable as Rstudio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
            'pandas>=0.20.0',  #所需要包的版本号
            'numpy>=1.14.0'   #所需要包的版本号
    ],
)