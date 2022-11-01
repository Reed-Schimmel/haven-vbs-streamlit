from pathlib import Path
from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]


# docs_packages = ["mkdocs==1.3.0", "mkdocstrings==0.18.1"]# TODO: configure and use
# style_packages = ["black==22.3.0", "flake8==3.9.2", "isort==5.10.1"]# TODO: configure and use
# test_packages = ["pytest==7.1.2", "pytest-cov==2.10.1", "great-expectations==0.15.15"]# TODO: configure and use


# Define our package
setup(
    name="vault-backed-shoring",
    version="0.1.0",
    description="Calculates (On/Off)Shore for Haven Protocol 3.0",
    author="Reed Schimmel",
    author_email="reed+vbs@simplelogin.com",
    url="https://github.com/Reed-Schimmel/haven-vbs-streamlit",
    python_requires=">=3.10",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    # extras_require={
    #     "dev": docs_packages + style_packages + test_packages + ["pre-commit==2.19.0"],
    #     "docs": docs_packages,
    #     "test": test_packages,
    # },
)
