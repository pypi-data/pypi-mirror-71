from setuptools import setup
import sys

assert sys.version_info >= (3, 6, 0), "black_nbconvert requires Python 3.6+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name="rename_github_default_branch",
    use_scm_version=True,
    description="A Python script for bulk renaming the default branch of your "
    "GitHub repositories using the API",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Dan Foreman-Mackey",
    author_email="foreman.mackey@gmail.com",
    url="https://github.com/dfm/rename_github_default_branch",
    license="MIT",
    py_modules=["rename_github_default_branch"],
    python_requires=">=3.6",
    zip_safe=False,
    install_requires=["requests", "click", "tqdm"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={
        "console_scripts": [
            "rename-github-default-branch=rename_github_default_branch:main"
        ]
    },
)
