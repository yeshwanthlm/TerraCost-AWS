#!/usr/bin/env python3
"""
Setup script for AWS Terraform Cost Analyzer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="terraform-cost-analyzer",
    version="1.0.0",
    author="Yeshwanth L M",
    author_email="yeshwanthlm@gmail.com",
    description="AI-powered AWS cost estimation tool for Terraform plans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yeshwanthlm/TerraCost-AWS",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    keywords="aws terraform cost analysis bedrock ai cloud infrastructure",
    python_requires=">=3.8",
    install_requires=requirements,
    license="MIT",
    entry_points={
        "console_scripts": [
            "terraform-cost-analyzer=terraform_cost_analyzer:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yeshwanthlm/TerraCost-AWS/issues",
        "Source": "https://github.com/yeshwanthlm/TerraCost-AWS",
        "Documentation": "https://github.com/yeshwanthlm/TerraCost-AWS/blob/main/README.md",
    },
)