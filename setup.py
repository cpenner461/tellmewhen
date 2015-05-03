from setuptools import setup, find_packages

setup(
    name='tellmewhen',
    version='0.1',
    description='A simple tool to watch web resources and notify you when they change.',
    author="Charlie Penner",
    author_email="charles.penner@gmail.com",
    url='http://cpenner461.github.io/tellmewhen/',
    keywords=[],
    classifiers=[],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'Click==4.0',
        'Flask==0.10.1',
        'Requests==2.6.2',
        'Keyring==5.3',
    ],
    entry_points='''
        [console_scripts]
        tmw=tmw.cli:cli
    ''',
)

