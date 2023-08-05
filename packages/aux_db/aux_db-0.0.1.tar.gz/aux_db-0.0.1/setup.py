# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    packages=find_packages(),
    name='aux_db',
    version='0.0.1',
    author='LiaoDingyi',
    author_email='731737792@qq.com',
    py_modules=[r'aux_db\db'],
    description="auxiliary sqlserver tool",
    platforms='window',
    install_requires=['pymssql'],
    classifiers=[],
    url='https://github.com/yituocpuls'
)
