from pathlib import Path
from setuptools import find_packages, setup


# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="fifa-editor-updater",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version="0.0.1",
    description="Fifa editor updater",
    author="lukacat10",
    author_email="lukacat100@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/lukacat100/folder-scanner",
    },
    classifiers=[
        "Programming Language :: Python :: 3.11.2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "PyGithub>=1.59.0",
        "pywin32>=306",
        "urllib3>=2.0.3",
        "packaging>=23.1",
        "dataclass-wizard>=0.22.2",
    ],
    extras_require={"dev": ["IPython"]},
    entry_points={
        "console_scripts": [
            "fifa_editor_updater = main:main",
        ]
    },
)
