import setuptools

setuptools.setup(
    name="doulma",
    version="0.1.0-rc-4",
    description="A Light Weight Python Utility Library.",
    long_description="A Light Weight Python Utility Library.",
    author="HussainARK",
    author_email="hussain.ark@yahoo.com",
    license="MIT",
    url="https://github.com/HussainARK/doulma",
    packages=['tests'],
    scripts=['__init__', 'cli', 'exceptions', 'hashing', 'network', 'variables'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
