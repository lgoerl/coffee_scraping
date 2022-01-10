from setuptools import find_packages
from setuptools import setup

setup(
    name="coffee_scraping",
    version="0.0.1",
    description="scrape coffee roaster data",
    url="https://github.com/lgoerl/coffee_scraping",
    python_requires=">=3.7",
    author="Lee Goerl",
    packages=find_packages(exclude=["docs", "tests"]),
    package_dir={"dags": "dags"},
)
