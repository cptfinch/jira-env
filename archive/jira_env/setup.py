from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Core requirements
core_requirements = [
    "requests>=2.25.0",
    "pyyaml>=5.4.0",
]

# Extension-specific requirements
rag_requirements = [
    "openai>=1.0.0",
    "numpy>=1.20.0",
    "scikit-learn>=1.0.0",
    "faiss-cpu>=1.7.0",
    "langchain>=0.0.200",
]

web_requirements = [
    "flask>=2.0.0",
    "streamlit>=1.0.0",
    "plotly>=5.0.0",
    "pandas>=1.3.0",
]

chat_requirements = [
    "slack-sdk>=3.0.0",
    "botbuilder-core>=4.14.0",
    "discord.py>=2.0.0",
]

interactive_requirements = [
    "prompt_toolkit>=3.0.0",
    "rich>=10.0.0",
    "inquirer>=2.7.0",
]

# All requirements (for development)
all_requirements = core_requirements + rag_requirements + web_requirements + chat_requirements + interactive_requirements

setup(
    name="jira-env",
    version="0.1.0",
    author="cptfinch",
    author_email="your.email@example.com",  # Update with your email
    description="A comprehensive interface to the Jira API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cptfinch/jira-env",
    packages=find_packages(),
    package_data={
        "jira_env": ["data/*.yaml"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=core_requirements,
    extras_require={
        "rag": rag_requirements,
        "web": web_requirements,
        "chat": chat_requirements,
        "interactive": interactive_requirements,
        "all": all_requirements,
    },
    entry_points={
        "console_scripts": [
            "jira-interface=jira_env.cli:main",
            "jira-export=jira_env.export_manager:main",
            "jira-web=jira_env.web.interface:main",
        ],
    },
) 