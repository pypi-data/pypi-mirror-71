import re
import os.path

from setuptools import setup, find_packages


with open(
    os.path.join(os.path.dirname(__file__), 'grpclib', '__init__.py')
) as f:
    VERSION = re.match(r".*__version__ = '(.*?)'", f.read(), re.S).group(1)

with open(
    os.path.join(os.path.dirname(__file__), 'README.rst')
) as f:
    DESCRIPTION = f.read()

setup(
    name='grpclib',
    version=VERSION,
    description='Pure-Python gRPC implementation for asyncio',
    long_description=DESCRIPTION,
    long_description_content_type='text/x-rst',
    author='Vladimir Magamedov',
    author_email='vladimir@magamedov.com',
    url='https://github.com/vmagamedov/grpclib',
    packages=find_packages(),
    package_data={'grpclib': ['py.typed']},
    license='BSD-3-Clause',
    python_requires='>=3.6',
    install_requires=[
        'h2',
        'multidict',
        'dataclasses;python_version<"3.7"',
    ],
    entry_points={
        'console_scripts': [
            # backward compatibility
            'protoc-gen-python_grpc=grpclib.plugin.main:main',
            'protoc-gen-grpclib_python=grpclib.plugin.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
