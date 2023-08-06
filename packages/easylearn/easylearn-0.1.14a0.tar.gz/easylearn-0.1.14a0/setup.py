#-*- coding:utf-8 -*-

"""
Created on 2020/03/03
------
@author: Chao Li; Mengshi Dong; Shaoqiang Han; Lili Tang; Ning Yang; Peng Zhang; Weixiang Liu    
Email:  lichao19870617@gmail.com; dongmengshi1990@163.com; 867727390@qq.com; 
        lilyseyo@gmail.com; 1157663200@qq.com; 1597403028@qq.com; wxliu@szu.edu.cn.   
"""

from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name='easylearn',
    version='0.1.14.alpha',
    description=(
        'This project is designed for machine learning in resting-state fMRI field'
    ),
    # long_description=long_description,
    long_description_content_type="text/markdown",
    author='Chao Li',
    author_email='lichao19870617@gmail.com',
    maintainer='Chao Li; Mengshi Dong; Shaoqiang Han; Lili Tang; Ning Yang; Peng Zhang',
    maintainer_email='lichao19870617@gmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/easylearn-fmri/',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    install_requires=[
        'joblib',
        'numpy',
        'pandas',
        'python-dateutil',
        'pytz',
        'scikit-learn',
        'scipy',
        'six',
        'nibabel',
        'imbalanced-learn',
        'skrebate',
        'matplotlib',
        ],
)