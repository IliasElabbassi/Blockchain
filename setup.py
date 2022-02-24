import setuptools

setuptools.setup(
    include_package_data=True,
    name="Rv_bc",
    version="0.0.1",
    description="blockchain framework",
    author="Ilias El Abbassi",
    author_email="iliaselabbassi@outlook.fr",
    packages=setuptools.find_packages(),
    install_requires=[
        "Flask",
        "requests",
        "base58",
        "pycryptodome"
    ]
)