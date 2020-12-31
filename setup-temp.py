"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
from pip.req import parse_requirements

REQS = [str(ir.req) for ir in parse_requirements('requirements.txt',
                                                 session='hack')]
REQS2 = [str(ir.req) for ir in parse_requirements('dev-requirements.txt',
                                                  session='hack')]



setup(
    name='pmsplus-server',
    version='0.0.2',
    description='pms plus',
    url='',
    author='Ray Yen',
    author_email='ray.yen@acer.com',
    license='MIT',
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    install_requires=REQS,
    extras_require={
        'test': REQS2
    }
)
