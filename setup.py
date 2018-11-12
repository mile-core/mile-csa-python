import os
import re
import sys
import platform
import subprocess

from distutils.version import LooseVersion
from setuptools import setup, find_packages,  Extension
from setuptools.command.build_ext import build_ext

#
# http://www.benjack.io/2017/06/12/python-cpp-tests.html
#


cmake_build_tmp = ''


class CMakeExtension(Extension):

    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):

    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)',
                                                   out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(self.extensions[0])

    def build_extension(self, ext):

        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(
                cfg.upper(),
                extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()

        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''),
            self.distribution.get_version())

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(['cmake', ext.sourcedir+'/src/mile-csa-api'] + cmake_args,
                              cwd=self.build_temp, env=env)

        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp)

        global cmake_build_tmp
        cmake_build_tmp = self.build_temp

        print()  # Add an empty line for cleaner output


milecsa_api = CMakeExtension('milecsa_cpp')

setup(
    name='milecsa',
    version='1.1',
    description='MileCsa API',
    ext_modules=[
        milecsa_api,
    ],
    cmdclass=dict(build_ext=CMakeBuild),
)

libraries = ['milecsa']

print("Platform: ", platform.system())
print("Libraries: ", libraries)

include_dirs = [
    '/usr/include',
    '/usr/local/include',
    './src/mile-csa-api/include',
    './src/mile-csa-api/vendor/mile-crypto/include',
    './src/mile-csa-api/vendor/mile-crypto/src/private_include',
    './src/mile-csa-api/vendor/mile-crypto/src/ed25519/include',
    './src/mile-csa-api/vendor/nlohmann'
]

extra_link_args = []

if platform.system() == 'Darwin':
    extra_link_args += ['-stdlib=libc++']
    include_dirs += ['/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1']

milecsa_module = Extension(
    '__milecsa',
    language='c++',
    include_dirs=include_dirs,
    extra_compile_args=['-std=c++17'],
    extra_link_args=extra_link_args,
    sources=['src/lib/milecsa.cpp'],
    libraries=libraries,
    library_dirs=[cmake_build_tmp, cmake_build_tmp+'/lib', '/usr/lib'],
    py_limited_api=False)


setup(
    name='milecsa',
    version='0.7.1',
    author="Lotus Mile",
    license="MIT",
    description='Python Package Mile C Extension',
    url="http://mile.global",
    packages=find_packages(),
    include_package_data=True,
    ext_modules=[
        milecsa_module
    ],
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
)
