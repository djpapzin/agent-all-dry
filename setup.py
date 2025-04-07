from setuptools import setup, find_packages

setup(
    name="drying-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "openai>=1.0.0",
        "gradio>=4.0.0",
        "diffusers>=0.24.0",
        "python-dotenv>=1.0.0",
        "pytest>=7.0.0",
        "pillow>=10.0.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "isort>=5.12.0",
    ],
) 