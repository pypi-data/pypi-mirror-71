from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="ge25519",
    version="0.1.0",
    packages=["ge25519",],
    install_requires=["fe25519","parts","bitlist","fountains",],
    license="MIT",
    url="https://github.com/nthparty/ge25519",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Native Python implementation of Ed25519 "+\
                "group elements and operations.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
