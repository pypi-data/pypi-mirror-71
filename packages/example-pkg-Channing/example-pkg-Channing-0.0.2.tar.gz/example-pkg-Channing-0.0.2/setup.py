# coding=gbk
"""
author(����): Channing Xie(л�)
time(ʱ��): 2020/6/17 21:08
filename(�ļ���): setup.py.py
function description(��������):
...
"""
import setuptools

with open("README.md", 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-Channing",
    version="0.0.2",
    author="Channing",
    author_emain="M201972194@hust.edu.cn",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XieChen10983/packages",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
