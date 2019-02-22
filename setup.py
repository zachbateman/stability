'''
setup.py for stability package
'''
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    author="Zach Bateman",
    author_email='zkbateman@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python package enhancing workflow organization and presentation facilitation",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='stability', 'workflow', 'file', 'presentation', 'organize', 'gui', 'application',
    name='stability',
    packages=find_packages(include=['stability']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/zachbateman/stability',
    version='0.1.0',
)
