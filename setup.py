from setuptools import setup

setup(
    name='tellmewhen',
    version='0.1',
    py_modules=['tellmewhen'],
    install_requires=[
        'Click==4.0',
        'Flask==0.10.1',
        'Requests==2.6.2',
    ],
    entry_points='''
        [console_scripts]
        tmw=tmw.cli:cli
    ''',
)

