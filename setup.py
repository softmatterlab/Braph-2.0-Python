from setuptools import setup, find_packages

setup(
    name='braphy',
    version='2.0',
    description='A graph theory software for the analysis of brain connectivity',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pyinstaller', 'pyopengl', 'pyqtgraph', 'numpy'],
)
