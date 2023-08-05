from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="RSA-light-iot",
    version="1.0.1",
    description="A Python package to implement RSA Lightweight adapted for Public key Cryptography in IoT devices.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Defcon27/SITS-Secure-IoT-System",
    author="Hemanth Kollipara",
    author_email="hemanthkollipara95@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["RSA_light_iot"],
    include_package_data=True,
    install_requires=[""],

)
