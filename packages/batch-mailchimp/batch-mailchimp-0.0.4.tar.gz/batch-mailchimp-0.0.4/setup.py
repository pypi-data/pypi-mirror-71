from setuptools import setup, find_packages
from os.path import abspath, dirname, join


path = abspath(dirname(__file__))
with open(join(path, 'README.rst')) as f:
    readme = f.read()

setup(
    name='batch-mailchimp',
    description='A python client for v3 of MailChimp API, with batch support',
    url='https://github.com/andylolz/python-batchmailchimp',
    author='Andy Lulham',
    author_email='a.lulham@gmail.com',
    version='0.0.4',
    packages=find_packages(),
    license='MIT',
    keywords='mailchimp api v3 client wrapper',
    long_description=readme,
    install_requires=['mailchimp3>=2.0.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
