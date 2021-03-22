from pathlib import Path
import setuptools

requirements_file = Path(__file__).parent / "requirements.txt"
with open(requirements_file) as f:
    install_requires = f.read().strip().split("\n")

setuptools.setup(
    name="src",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
)
