from setuptools import setup

setup(
    name='demyst-entity',

    version='0.8.33.a6',

    description='',
    long_description='',

    author='Demyst Data',
    author_email='info@demystdata.com',

    license='',
    packages=['demyst.entity'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
    ],
    extras_require={
        'testing': [
            'pyspark==2.4.4'
            ]
        }
)
