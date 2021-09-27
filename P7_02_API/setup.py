from setuptools import setup, find_packages

setup(
    name='HeraProject',
    version='0.0.1',
    description='RESTful API based on Flask-RESTPlus to respond EFELYA\'s needs',
    url='',
    author='Florian Formentini',
    packages=find_packages(),

    include_package_data=True,  # including static/templates folders declared in MANIFEST.in

)
