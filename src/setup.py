from setuptools import setup, find_packages

setup(
    name='flick-integration',
    version='0.1.0',
    description='A sudden sharp movement.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'flick = main:cli'
        ],
    },
)