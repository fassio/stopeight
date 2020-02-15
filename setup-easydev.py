#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing','stopeight.util','stopeight.util.editor','stopeight.util.editor.modules']

import os
#cmake start
__import__('cmake')
from cmake import CMakeExtension, CMakeBuild
#cmake end

from setuptools import setup, Extension
import site

setup( name='stopeight',
       use_scm_version=True,
       description='stopeight: Comparing sequences of points in 2 dimensions',
       long_description='stopeight: Comparing sequences of points in 2 dimensions by visually overlapping them using matrix transformations (translation, scaling and rotation) and getting a boolean result.',
       author='Fassio Blatter',
       author_email='fassio@specpose.com',
       license='GNU General Public License, version 2',
       url='https://github.com/specpose/stopeight',
       python_requires='>=2.7',
       classifiers=[
           "Development Status :: 3 - Alpha",
           "Intended Audience :: Developers",
           "Topic :: Multimedia :: Sound/Audio :: Analysis",
           "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
           "Programming Language :: Python :: 2.7",
           "Programming Language :: Python :: 3",
           ],
       keywords="signal-analysis pen-stroke",
       packages=_packages,
       data_files=[(str(site.getusersitepackages()),['stopeight.pth'])],#required by stopeight-clibs if enabled in CMakeLists.txt
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },
       setup_requires=[
           'setuptools_scm',
           ],
       zip_safe=False,
#pip start - not in cmake_examples
       install_requires=[
          'numpy<1.17.0',#python2
          'future',
          'funcsigs',
          'matplotlib<3.0',#python2
          'PyQt5<5.11.0',# <5.11.0, because pip>=19.3 #not for python2
          ],
#pip end - not in cmake_examples
#cmake start
       ext_modules=[CMakeExtension('stopeight.matrix',libraries=['stopeight-clibs-matrix']),CMakeExtension('stopeight.grapher',libraries=['stopeight-clibs-grapher']),CMakeExtension('stopeight.analyzer',libraries=['stopeight-clibs-analyzer']),CMakeExtension('stopeight.legacy',libraries=['stopeight-clibs-legacy'])],
       cmdclass=dict(build_ext=CMakeBuild),
#cmake end
)
