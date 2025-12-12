### 3. setup.py
'''python'''
from setuptools import setup, find_packages

setup(
    name="qpat",
    version="0.1.0",
    author="amlabdr",
    description="Quantum Photonic Analysis Toolkit for quantum network characterization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amlabdr/qpat",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "qutip>=4.6.0",
        "pyyaml>=5.4.0",
    ],
    python_requires=">=3.8",
)