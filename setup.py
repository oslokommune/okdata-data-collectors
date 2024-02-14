from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="okdata-data-collectors",
    version="0.1.0",
    author="Oslo Origo",
    author_email="dataplattform@oslo.kommune.no",
    description="Data collector jobs for the Origo dataplatform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/okdata-data-collectors",
    packages=find_packages(),
    install_requires=["aws-xray-sdk", "boto3", "okdata-aws>=2,<3", "aiohttp>=3.9,<4"],
    python_requires=">=3.11",
)
