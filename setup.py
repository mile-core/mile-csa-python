import os
import platform
import subprocess
import sys

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

__version__ = '0.8.0'
__milecsa_api_version__ = '1.1.3'

darwin_flags = ['-mmacosx-version-min=10.12']


class ExtensionWithLibrariesFromSources(Extension):
    """Win is unsupported"""
    def __init__(self, name, sources, *args, **kw):
        self.libraries_from_sources = kw.pop('libraries_from_sources', [])

        if platform.system() == 'Darwin':
            kw['extra_link_args'] = kw.get('extra_link_args', []) + darwin_flags
            kw['include_dirs'] = kw.get('include_dirs', []) + [
                '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1'
            ]

        super().__init__(name, sources, *args, **kw)

    def build_libraries(self, ext_builder: build_ext):
        self.check_cmake_version()

        libraries = []
        libraries_dirs = ['/usr/lib']

        for lib_name, lib_path, lib_version in self.libraries_from_sources:
            libraries += [lib_name]
            libraries_dirs += self.build_library(
                ext_builder, lib_name, os.path.abspath(lib_path), lib_version
            )

        return libraries, libraries_dirs

    @staticmethod
    def build_library(ext_builder: build_ext, lib_name, lib_path, lib_version):
        build_temp = os.path.join(ext_builder.build_temp, lib_name)

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + build_temp,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if ext_builder.debug else 'Release'
        build_args = ['--config', cfg]

        cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
        build_args += ['--', '-j2']

        env = os.environ.copy()

        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''), lib_version
        )

        if not os.path.exists(build_temp):
            os.makedirs(build_temp)

        subprocess.check_call(['cmake', lib_path] + cmake_args,
                              cwd=build_temp, env=env)

        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=build_temp)

        return [build_temp, build_temp + '/lib']

    def check_cmake_version(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extension: " + self.name
            )


class BuildExt(build_ext):
    def build_extension(self, ext: Extension):
        if type(ext) is ExtensionWithLibrariesFromSources:
            ext: ExtensionWithLibrariesFromSources
            libraries, library_dirs = ext.build_libraries(self)
            ext.libraries += libraries
            ext.library_dirs += library_dirs
        super().build_extension(ext)


extra_compile_args = ['-std=c++17', '-DVERSION_INFO="{}"'.format(__version__)]

if platform.system() == 'Darwin':
    extra_compile_args = extra_compile_args + darwin_flags

ext_modules = [
    ExtensionWithLibrariesFromSources(
        '__milecsa',
        ['./src/milecsa_bindings/bindings.cpp'],
        include_dirs=[
            'src/pybind11/include',

            '/usr/include',
            '/usr/local/include',
            './src/mile-csa-api/include',
            './src/mile-csa-api/vendor/mile-crypto/include',
            './src/mile-csa-api/vendor/mile-crypto/src/private_include',
            './src/mile-csa-api/vendor/mile-crypto/src/ed25519/include',
            './src/mile-csa-api/vendor/nlohmann'
        ],
        language='c++',
        extra_compile_args=extra_compile_args,
        libraries_from_sources=[
            ('milecsa', './src/mile-csa-api', __milecsa_api_version__),
        ]
    ),
]


setup(
    name='milecsa',
    version=__version__,
    author="Lotus Mile",
    license="MIT",
    description='Python Package Mile C Extension',
    url="http://mile.global",
    packages=['milecsa'],
    ext_modules=ext_modules,
    install_requires=[
        'urllib3',
        'requests',
        'pillow',
        'qrcode'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={'build_ext': BuildExt},
)
