from os import path
import setuptools

here = path.abspath(path.dirname(__file__))

long_description = ''
with open(path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()
assert long_description

setuptools.setup(
    name="thor-devkit",
    version="0.9.3",
    author="laalaguer",
    author_email="laalaguer@gmail.com",
    description="SDK to interact with VeChain Thor public blockchain.",
    keywords="vechain thor blockchain sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/laalaguer/thor-devkit.py",
    project_urls={
        'Documentation': 'https://github.com/laalaguer/thor-devkit.py',
        'Source': 'https://github.com/laalaguer/thor-devkit.py',
        'Issue Tracker': 'https://github.com/laalaguer/thor-devkit.py/issues',
    },
    python_requires='>=3.6',
    install_requires=[x.strip() for x in open('requirements.txt')],
    packages=setuptools.find_packages('.'),
)