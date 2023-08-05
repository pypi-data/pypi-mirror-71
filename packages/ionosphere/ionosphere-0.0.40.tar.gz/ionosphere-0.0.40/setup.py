from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='ionosphere',
    version="0.0.40",
    description="Azure Resource Manager Template creation library",
    long_description=readme(),
    author="Alex Azarh",
    author_email="alex.az@quali.com",
    url="https://github.com/qualinext/ionosphere",
    license="New BSD license",
    packages=['ionosphere', 'ionosphere.helpers'],
    scripts=['scripts/cfn', 'scripts/cfn2py'],
    install_requires=["enum34==1.1.6"],
    test_suite="tests",
    tests_require=[],
    extras_require={'policy': ['awacs']},
    use_2to3=True,
)
