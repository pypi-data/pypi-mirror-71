import os
import io
import setuptools


name = "tmg-etl-pipeline"
description = "TMG ETL pipeline"
version = "0.0.1"
dependencies = [
    "cachetools==4.1.0",
    "certifi==2020.4.5.1",
    "chardet==3.0.4",
    "google-api-core==1.17.0",
    "google-auth==1.15.0",
    "google-cloud-core==1.3.0",
    "google-cloud-logging==1.15.0",
    "google-cloud-secret-manager==1.0.0",
    "googleapis-common-protos==1.51.0",
    "grpc-google-iam-v1==0.12.3",
    "grpcio==1.29.0",
    "idna==2.9",
    "protobuf==3.12.1",
    "pyasn1==0.4.8",
    "pyasn1-modules==0.2.8",
    "pytz==2020.1",
    "PyYAML==5.3.1",
    "requests==2.23.0",
    "rsa==4.0",
    "six==1.15.0",
    "urllib3==1.25.9"
]

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()


setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author='TMG Data Platform team',
    author_email="data.platform@telegraph.co.uk",
    license="Apache 2.0",
    url='https://github.com/telegraph/tmg-etl-pipeline',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    install_requires=dependencies,
    python_requires='>=3.6',
)
