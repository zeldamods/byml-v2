import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="byml",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
    install_requires=['PyYAML~=6.0', 'sortedcontainers~=2.0', 'oead~=1.1'],
    entry_points = {
        'console_scripts': [
            'byml_to_yml = byml.byml_to_yml:main',
            'yml_to_byml = byml.yml_to_byml:main'
        ]
    },
)
