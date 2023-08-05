import subprocess
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.extension import Extension

with open("README.rst", "r") as f:
    readme = f.read()

CURRENT_DIR = Path(__file__).parent


class MakeInstall(install):
    def run(self):
        subprocess.check_call(
            ["make"], cwd=(CURRENT_DIR / "3DAlignment").as_posix()
        )
        subprocess.check_call(
            ["make", "release"], cwd=(CURRENT_DIR / "3DAlignment").as_posix()
        )

        subprocess.check_call(
            ["make"], cwd=(CURRENT_DIR / "LightField").as_posix()
        )
        subprocess.check_call(
            ["make", "release"], cwd=(CURRENT_DIR / "LightField").as_posix()
        )

        super().run()


setup(
    name="light-field-distance",
    version="0.0.3",
    author="Kacper Kania",
    license="BSD",
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
    zip_safe=False,
    include_package_data=True,
    cmdclass={"install": MakeInstall},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: C",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Typing :: Typed",
    ],
)
