import glob
import os

from setuptools import setup, find_packages

MPINT_DIR = os.path.dirname(os.path.abspath(__file__))

with open('README.rst','r') as fh:
    long_description = fh.read()

setup(
    name="MPInterfaces",
    version="2020.6.19",
    install_requires=["FireWorks>=1.4.0",
                      "custodian>=1.0.1", "pymatgen-db>=0.5.1",
                      "ase>=3.11.0", "six", "pyhull>=1.5.3",
		      "seaborn","pyyaml", "nose"],
    extras_require={"babel": ["openbabel", "pybel"],
                    "remote": ["fabric"],
                    "doc": ["sphinx>=1.3.1", "sphinx-rtd-theme>=0.1.8"]
                    },
    author="Kiran Mathew, Joshua J. Gabriel, Michael Ashton, "
           "Arunima K. Singh, Joshua T. Paul, Seve G. Monahan, "
           "Richard G. Hennig, Venkata Surya Chaitanya Kolluru",
    author_email="joshgabriel92@gmail.com, kmathew@lbl.gov, ashtonmv@gmail.com,kvs.chaitanya@ufl.edu,joshuapaul@ufl.edu",
    maintainer="Venkata Surya Chaitanya Kolluru, Joshua T. Paul",
    maintainer_email="kvs.chaitanya@ufl.edu,joshuapaul@ufl.edu",
    description=(
        "High throughput analysis of interfaces using VASP and Materials Project tools"),
    license="MIT",
    url="https://github.com/henniggroup/MPInterfaces",
    packages=find_packages(),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",        
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    scripts=glob.glob(os.path.join(MPINT_DIR, "mpinterfaces", "scripts", "*"))
)
