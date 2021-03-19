from setuptools import setup, find_packages

setup(
    name='tellmewhen',
    version='0.2',
    description='A simple tool to watch web resources and notify you when they change.',
    author="Charlie Penner",
    author_email="charles.penner@gmail.com",
    url='http://cpenner461.github.io/tellmewhen/',
    keywords=[],
    classifiers=[],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'Click==7.0',
        'Flask==1.1.1',
        'Requests==2.22.0',
        'Keyring==19.2.0',
        'Jinja2==2.11.3',
    ],
    entry_points='''
        [console_scripts]
        tmw=tmw.cli:cli
    ''',
)

