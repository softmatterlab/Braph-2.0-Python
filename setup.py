from setuptools import setup, find_packages

setup(
    name='braphy',
    version='2.0',
    description='A graph theory software for the analysis of brain connectivity',
    packages=find_packages(),#['braphy', 'braphy.graph', 'braphy.graph_measures', 'test'],
    install_requires=['numpy'],
)
