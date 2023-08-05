from setuptools import setup, find_packages
import subprocess
from setuptools.command.install import install

with open("README.rst", "r") as f:
    readme = f.read()


class MakeInstall(install):
    def run(self):
        install.run(self)
        subprocess.check_call(["make"], cwd="3DAlignment")
        subprocess.check_call(["make", "release"], cwd="3DAlignment")

        subprocess.check_call(["make"], cwd="LightField")
        subprocess.check_call(["make", "release"], cwd="LightField")


setup(
    name="light-field-distance",
    version="0.0.2",
    author="Kacper Kania",
    license=u"BSD",
    packages=find_packages(
        exclude=["3DAlignment", "Executable", "LightField"]
    ),
    install_requires=["trimesh>=3.6.43"],
    long_description=readme,
    description=(
        "light-field-distance is a BSD-licensed package for "
        "calculating Light Field Distance from two Wavefront OBJ "
        "meshes using OpenGL"
    ),
    cmdclass={"install": MakeInstall},
    classifiers=[
        u"Development Status :: 4 - Beta",
        u"Environment :: Console",
        u"Intended Audience :: Developers",
        u"Intended Audience :: Education",
        u"Intended Audience :: Science/Research",
        u"License :: OSI Approved :: BSD License",
        u"Operating System :: MacOS :: MacOS X",
        u"Operating System :: Microsoft :: Windows",
        u"Operating System :: POSIX",
        u"Programming Language :: C",
        u"Programming Language :: Python :: 3",
        u"Topic :: Multimedia :: Graphics :: 3D Rendering",
        u"Topic :: Scientific/Engineering",
        u"Topic :: Scientific/Engineering :: Information Analysis",
        u"Typing :: Typed",
    ],
)
