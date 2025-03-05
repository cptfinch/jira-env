from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jira-interface",
    version="0.1.0",
    author="cptfinch",
    author_email="your.email@example.com",  # Update with your email
    description="A command-line tool for interacting with Jira's REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cptfinch/jira-env",
    py_modules=["jira-interface"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "jira-interface=jira-interface:main",
        ],
    },
) 