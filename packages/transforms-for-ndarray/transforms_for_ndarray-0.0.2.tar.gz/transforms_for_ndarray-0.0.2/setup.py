# coding=gbk
"""
author(����): Channing Xie(л�)
time(ʱ��): 2020/6/18 10:11
filename(�ļ���): setup.py
function description(��������):
...
"""
from setuptools import setup, find_packages

setup(
    name="transforms_for_ndarray",
    version="0.0.2",
    description=(
        "transformations for numpy ndarray."
    ),
    long_description=open("README.md", encoding='utf-8').read(),
    author="ChanningXieChen",
    author_emain="M201972194@hust.edu.cn",
    license="MIT License",
    packages=find_packages(),
    platforms=["all"],
    url="https://github/XieChen10983/packages",
    install_requires=[
        'pytorch>=1.5.0',
        'numpy>=1.18.5',
        'opencv>=3.4.2',
        'Pillow>=7.1.2',
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ]
)
