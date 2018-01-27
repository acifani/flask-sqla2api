from setuptools import setup

setup(
    name='Flask-SQLA2api',
    version='0.2.0',
    url='https://github.com/acifani/flask-sqla2api',
    license='BSD',
    author='Alessandro Cifani',
    author_email='alessandro.cifani@gmail.com',
    description='Flask-SQLAlchemy Model to API in one line of code',
    packages=['flask_sqla2api'],
    install_requires=[
        'Flask>=0.12.2',
        'Flask-SQLAlchemy>=2.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python'
    ],
    extras_require={
        'test': ['pytest']
    }
)
