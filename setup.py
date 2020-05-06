from setuptools import setup, find_packages

setup(
    name='braphy',
    version='2.0',
    description='A graph theory software for the analysis of brain connectivity',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['openpyxl>=3.0.3', 'pandas>=1.0.2', 'pyopengl>=3.1.5', 'pyqtgraph>=0.10.0', 'numpy>=1.18', 'xlrd>=1.2.0', 'matplotlib>=3.2.1', 'pyqt5==5.13'],
)
