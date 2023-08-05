from setuptools import setup
import setuptools

setup(
    name = 'mysqlctl',
    version = '2.0.2',
    author = '王哈哈',
    author_email = 'mail65656@163.com',
    description = '用来操作MySQL增删改查',
    long_description = '用来操作MySQL增删改查',
    packages = setuptools.find_packages(),
    platforms = 'any',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        # 你的库依赖的第三方库（也可以指定版本）'
        'pymysql'
    ],
)

