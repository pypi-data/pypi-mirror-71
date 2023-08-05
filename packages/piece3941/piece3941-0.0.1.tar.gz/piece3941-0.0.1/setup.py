# -*- coding: utf-8 -*-

import setuptools

account = "redfoxatasleep"
password = "github123456"
mail = "bbxxone@qq.com"
token = {
    "zhjh":"pypi-AgENdGVzdC5weXBpLm9yZwIkMDU5NTA1Y2QtNTM0ZC00OTZjLTkxMDYtMjNiOGViOTRiNTExAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiDK-r-EQhADC1kicp2zKhWoa27N50PgfgE-sxXCEw_xiA"
}

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="piece3941",
    version="0.0.1",
    author="redfoxatasleep",
    author_email="bbxxone@qq.com",
    description="Useful Code Piece.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedFoxAtAsleep/piece",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)

