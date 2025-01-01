from setuptools import setup, find_packages

# Read requirements files
def read_requirements(filename: str) -> list:
    """Read requirements from a file and return as a list."""
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read long description from README
def read_long_description() -> str:
    """Read the README file and return its contents."""
    with open('README.md') as f:
        return f.read()

setup(
    name="rag_chatbot",
    version="1.0.0",
    description="A RAG-enabled chatbot using clean architecture",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/rag-chatbot",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=read_requirements("requirements/base.txt"),
    extras_require={
        "dev": read_requirements("requirements/dev.txt"),
        "prod": read_requirements("requirements/prod.txt"),
    },
    entry_points={
        "console_scripts": [
            "rag-chatbot=rag_chatbot.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)