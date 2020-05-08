#!/usr/bin/env python

import os
#distutils start
__import__('python')
from python import get_pybind_include, BuildExt
my_path = os.path.dirname(os.path.realpath(__file__))
import sysconfig
_include_dirs=[
    os.path.join(my_path,'stopeight-clibs','cmake-git-version-tracking','better-example'),
    # Path to pybind11 headers
    str(get_pybind_include()),
    str(get_pybind_include(user=True)),
]
_qt5_include_dirs=_include_dirs
_library_dirs=[]
_CONFINCLUDEDIR=sysconfig.get_config_var('CONFINCLUDEDIR')
_MULTIARCH=sysconfig.get_config_var('MULTIARCH')
_prefix=sysconfig.get_config_var('prefix')
if _CONFINCLUDEDIR!='None':
    if _MULTIARCH!='None':
        _qt5_include_dirs.append(os.path.join(str(_CONFINCLUDEDIR),str(_MULTIARCH),'qt5')) #ubuntu only
    _qt5_include_dirs.append(os.path.join(str(_CONFINCLUDEDIR),'qt')) #conda only
    _qt5_include_dirs.append(os.path.join(str(_CONFINCLUDEDIR)))
if _prefix!='None':
    _qt5_include_dirs.append(os.path.join(str(_prefix),'Library','include','qt'))#conda Windows only
    _library_dirs.append(os.path.join(str(_prefix),'Library','lib'))#conda Windows only
#distutils end

from setuptools import setup, Extension, find_namespace_packages

setup( use_scm_version=True,
       packages=find_namespace_packages(include=['stopeight.*']),
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },
       setup_requires=[
           'setuptools',
           'pybind11>=2.4',
           'setuptools_scm',
           ],
       zip_safe=False,
#distutils start
#pip start
       install_requires=[
          'numpy',
          'future',
          'funcsigs',
          'matplotlib',
          'pybind11>=2.4',
          'PyQt5',# >5.11.0: install with pip, not easy_setup!
          ],
#pip end
       ext_modules = [
           Extension(
               'stopeight.grapher',
               [os.path.join(my_path,'stopeight-clibs','grapher-wrappers','IFPyGrapher.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','grapher')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-grapher',
               'stopeight-clibs-matrix'],
               language='c++',
               optional=True
           ),
           Extension(
               'stopeight.matrix',
               [os.path.join(my_path,'stopeight-clibs','matrix-wrappers','IFPyMatrix.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','matrix')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-matrix'],
               language='c++',
               optional=True
           ),
           Extension(
               'stopeight.analyzer',
               [os.path.join(my_path,'stopeight-clibs','analyzer-wrappers','IFPyAnalyzer.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','include'),
                   os.path.join(my_path,'stopeight-clibs','analyzer')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-analyzer'],
               language='c++',
               optional=True
           ),
           Extension(
              'stopeight.legacy',
               [os.path.join(my_path,'stopeight-clibs','legacy-wrappers','interfacepython.cpp'),
               ],
               include_dirs=_qt5_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','legacy/include'),
                   os.path.join(my_path,'stopeight-clibs','legacy-wrappers')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-legacy','Qt5Core'],#Qt5Core needed for old wrapper
               language='c++',
               optional=True
              ),
            Extension(
              'stopeight.getters',
               [os.path.join(my_path,'stopeight-clibs','legacy-wrappers','IFPyGetters.cpp'),
               os.path.join(my_path,'stopeight-clibs','legacy-wrappers','IFPyShared.cpp')],
               include_dirs=_qt5_include_dirs + [
                   os.path.join(my_path,'stopeight-clibs','legacy/include'),
                   os.path.join(my_path,'stopeight-clibs','legacy-wrappers')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-legacy','stopeight-clibs-matrix','Qt5Core'],#Qt5Core needed for old wrapper
               language='c++',
               optional=True
              ),
       ],
       cmdclass={'build_ext': BuildExt},
#distutils end
)
