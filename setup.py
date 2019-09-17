import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gams_parser",
    version="1.0.0",
    author="Eric Anderson",
    author_email="eric@andersonopt.com",
    description="Gams parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['gams_parser'],
    package_dir={'gams_parser':'gams_parser'},
    install_requires=['lark-parser','pandas'],
    package_data={'gams_parser': ['grammar/*.lark']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
