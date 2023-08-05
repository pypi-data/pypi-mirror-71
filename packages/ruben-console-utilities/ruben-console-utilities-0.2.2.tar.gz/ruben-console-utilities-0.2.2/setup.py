import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruben-console-utilities",
    version="0.2.2",
    author="Ruben Dougall",
    author_email="info.ruebz999@gmail.com",
    description="Simple utility functions for command-line applications.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    keywords="console command-line utilities",
    project_urls={
        "Documentation": "https://python-console-utilities.readthedocs.io/",
        "Source Code": "https://github.com/Ruben9922/python-console-utilities",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.6',
    py_modules=["console_utilities"],
)
