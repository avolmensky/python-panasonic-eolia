""" Setup for python-panasonic-eolia """

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='panasoniceolia',
    version='0.0.1',
    description='Read and change status of Panasonic Eolia devices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/avolmensky/python-panasonic-eolia',
    author='avolmensky',
    license='MIT',
    classifiers=[
       'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='home automation panasonic eolia climate',
    install_requires=['requests>=2.20.0'],
    packages=['panasoniceolia'],
    package_data={'': ['certificatechain.pem']},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'panasoniceolia=panasoniceolia.__main__:main',
        ]
    })
