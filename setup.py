import setuptools

setuptools.setup(
    name="src",
    packages=setuptools.find_packages(),
    install_requires=[
        "attrs",
        "python-box",
        "rich",
        "pandarallel",
        "haversine",
        "torch",
        "pytorch_lightning",
        "pandas",
        "numpy",
        "scikit-learn",
        "dvclive",
        "neptune-client",
    ],
)
