# -- coding:utf-8 --
import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="milian-blockchain-sdk",  # Replace with your own username
    version="1.0.1",
    author="杭州米链科技有限公司",
    author_email="hzqixunda@163.com",
    description="链盟 Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "pycryptodome",
        "eth-account",
        "eth-utils",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
