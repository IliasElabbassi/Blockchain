import setuptools

setuptools.setup(
    include_package_data=True,
    name="Rv_bc",
    version="0.0.1",
    license="MIT",
    author="Ilias El Abbassi",
    description="blockchain framework",
    author_email="iliaselabbassi@outlook.fr",
    url="https://github.com/IliasElabbassi/Blockchain",
    packages=setuptools.find_packages(),
    install_requires=[
        "Flask",
        "requests",
        "base58",
        "pycryptodome"
    ]
)