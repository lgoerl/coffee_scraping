from setuptools import find_packages
from setuptools import setup

setup(
    name="roi_dags",
    version="0.0.1073",
    description="ROI dags repo",
    url="https://github.com/pepsico-ecommerce/roi",
    python_requires=">=3.7",
    author="Andrew Paslavsky",
    packages=find_packages(exclude=["docs", "tests"]),
    package_dir={"dags": "dags"},
)
