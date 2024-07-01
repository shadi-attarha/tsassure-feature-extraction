from setuptools import setup, find_packages

setup(
    name='tsassure_feature',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'openpyxl',
        # Add any additional dependencies here
    ],
    entry_points={
        'console_scripts': [
            'tsassure=tsassure_feature.main:main',
        ],
    },
)