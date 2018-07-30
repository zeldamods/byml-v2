import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="byml",
    version="2.0.0-3",
    author="leoetlino",
    author_email="leo@leolam.fr",
    description="A simple Nintendo BYML or BYAML v2/v3 parser and writer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leoetlino/byml-v2",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
    install_requires=['PyYAML~=3.12', 'sortedcontainers~=2.0', 'wszst_yaz0~=1.0'],
    entry_points = {
        'console_scripts': [
            'byml_to_yml = byml.__main__:byml_to_yml',
            'yml_to_byml = byml.__main__:yml_to_byml'
        ]
    },
)
