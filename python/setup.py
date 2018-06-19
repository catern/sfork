from setuptools import setup
from os import path

setup(name='sfork',
      version='0.1.0',
      description='An alternative approach to starting processes on Linux.',
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
      ],
      keywords='linux syscall processes',
      url='https://github.com/catern/sfork',
      author='catern',
      author_email='sbaugh@catern.com',
      license='MIT',
      cffi_modules=["ffibuilder.py:ffibuilder"],
      packages=['sfork', 'sfork.tests'])
