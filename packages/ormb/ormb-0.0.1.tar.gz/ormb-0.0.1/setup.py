import re
import os
from setuptools import find_packages
from setuptools import setup

from git_release import download
download()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), "ormb", "__init__.py")
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        raise RuntimeError("Cannot find version in {}".format(init_py))


setup(
    name="ormb",
    version=read_version(),
    url="https://github.com/caicloud/ormb",
    project_urls={
        "Documentation": "https://github.com/caicloud/ormb/wikis/home",
        "Code": "https://github.com/caicloud/ormb",
        "Issue tracker": "https://github.com/caicloud/ormb/issues",
    },
    maintainer="gaocegege, ZhuYuJin",
    description="ormb warehouse",
    python_requires=">=3.6",
    install_requires=[
        "requests"
    ],
    packages=find_packages(include=("ormb", "ormb.*")),
    package_data={'ormb': ['bin/*']},
)
