from setuptools import setup, find_packages

import os
import canarytokend

setup(
    name='canarytokend',
    version=canarytokend.__version__,
    url='http://www.thinkst.com/',
    author='Thinkst Applied Research',
    author_email='info@thinkst.com',
    description='Canarytoken daemon',
    long_description='A service to monitor logfiles and fire Canarytoken alerts.',
    install_requires=[
        "Twisted==15.2.1",
        "requests==2.7.0",
        "wsgiref==0.1.2",
        "zope.interface==4.1.2",
        "mysql==0.0.1",
        "MySQL-python==1.2.5",
    ],
    license='BSD',
    # setup.py doesn't auto-include nested dirs without the below
    packages = find_packages(exclude="test"),
    include_package_data=True,
    scripts=['bin/canarytokend'],
    platforms='linux',
    data_files=[('',['canarytokend/canarytokend.tac'])]
)
