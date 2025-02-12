from setuptools import setup

setup(
    install_requires=["pygame"],
    name='clibt',
    version='0.0.1',
    packages=['clibt'],
    url='',
    license='',
    author='hir12111',
    author_email='hir12111@gmail.com',
    description='',
    entry_points={'console_scripts':
                  ['seqdig=clibt.seqdig:main',
                   'seqimg=clibt.seqimg:main',
                   'seqlist=clibt.seqlist:main',
                   'seqtext=clibt.seqtext:main']}
)
