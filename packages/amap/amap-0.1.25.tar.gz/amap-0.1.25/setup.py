from setuptools import setup, find_namespace_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = [
    "nibabel",
    "numpy",
    "configparser",
    "pandas<=0.25.3,>=0.25.1",
    "scikit-image",
    "tqdm",
    "natsort",
    "multiprocessing-logging",
    "configobj",
    "slurmio",
    "brainio>=0.0.19",
    "fancylog",
    "micrometa",
    "imlib>=0.0.25",
    "dask>=2.15.0",
    "napari>=0.3.0",
    "scikit-image==0.16.2",
    "neuro>=0.0.13",
]


setup(
    name="amap",
    version="0.1.25",
    description="Automated mouse atlas propagation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={
        "dev": [
            "sphinx",
            "recommonmark",
            "sphinx_rtd_theme",
            "pydoc-markdown",
            "black",
            "pytest-cov",
            "pytest",
            "gitpython",
            "coverage",
        ]
    },
    python_requires=">=3.6, <3.8",
    packages=find_namespace_packages(exclude=("docs", "tests*")),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "amap = amap.cli:main",
            "amap_gui = amap.cli:gui",
            "amap_download = amap.download.cli:main",
        ]
    },
    project_urls={
        "Source Code": "https://github.com/SainsburyWellcomeCentre/amap-python",
        "Bug Tracker": "https://github.com/SainsburyWellcomeCentre/amap-python/issues",
    },
    author="Adam Tyson, Charly Rousseau, Christian Niedworok",
    author_email="adam.tyson@ucl.ac.uk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    zip_safe=False,
)
