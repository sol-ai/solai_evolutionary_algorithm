from setuptools import setup, find_packages

setup(
    name='solai_evolutionary_algorithm',
    version='0.1.0',
    packages=find_packages(
        include=['solai_evolutionary_algorithm', 'solai_evolutionary_algorithm.*']),
    package_data={'solai_evolutionary_algorithm': [
        'resources/*.json', 'resources/sample_characters/*.json']}
)
