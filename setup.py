# -*- coding: utf-8 -*-
"""Lawrence McDaniel https://lawrencemcdaniel.com."""
# pylint: disable=open-builtin
import io
import os
import sys
from setuptools import find_packages, setup, __version__ as setuptools_version
from distutils.command.install import INSTALL_SCHEMES
from distutils.command.install_data import install_data

from setup_utils import get_semantic_version

HERE = os.path.abspath(os.path.dirname(__file__))

if int(setuptools_version.split(".", 1)[0]) < 18:
    assert "bdist_wheel" not in sys.argv, "setuptools 18 or later is required for wheels."


class osx_install_data(install_data):
    """
    Fix macOS installation path.

    On MacOS, the platform-specific lib dir is at:
      /System/Library/Framework/Python/.../
    which is wrong. Python 2.5 supplied with MacOS 10.5 has an Apple-specific
    fix for this in distutils.command.install_data#306. It fixes install_lib
    but not install_data, which is why we roll our own install_data class.
    """

    def finalize_options(self):
        """
        Finalize options.

        By the time finalize_options is called, install.install_lib is set to
        the fixed directory, so we set the installdir to install_lib. The
        install_data class uses ('install_data', 'install_dir') instead.
        """
        self.set_undefined_options("install", ("install_lib", "install_dir"))
        install_data.finalize_options(self)


if sys.platform == "darwin":
    cmdclasses = {"install_data": osx_install_data}
else:
    cmdclasses = {"install_data": install_data}

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme["data"] = scheme["purelib"]


def load_readme():
    with io.open(os.path.join(HERE, "README.md"), "rt", encoding="utf8") as f:
        return f.read()


README = load_readme()


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split("#")[0].strip() for line in open(path).readlines() if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.
    Returns:
        bool: True if the line is not blank, a comment, a URL, or an included file
    """
    return not (
        line == ""
        or line.startswith("-c")
        or line.startswith("-r")
        or line.startswith("#")
        or line.startswith("-e")
        or line.startswith("git+")
    )


print("Found packages: {packages}".format(packages=find_packages()))

print("requirements found: {requirements}".format(requirements=load_requirements("requirements/common.in")))

setup(
    name="django-memberpress-client",
    version=get_semantic_version(),
    description="A Django plugin to add Memberpress REST API and Webhook integrations.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Lawrence McDaniel",
    author_email="lpm0073@gmail.com",
    maintainer="Jeff Cohen",
    maintainer_email="jcohen28@gmail.com",
    url="https://github.com/lpm0073/django-memberpress-client",
    project_urls={
        "Code": "https://github.com/lpm0073/django-memberpress-client",
        "Issue tracker": "https://github.com/lpm0073/django-memberpress-client/issues",
        "Community": "https://docs.memberpress.com/category/215-developer-resources",
    },
    license="MIT",
    license_files=("LICENSE.txt",),
    platforms=["any"],
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.html"]},  # include any Mako templates found in this repo.
    zip_safe=False,
    keywords="Python, Django, Wordpress, MemberPress, REST API",
    python_requires=">=3.8",
    install_requires=load_requirements("requirements/common.txt"),
    entry_points={
        # mcdaniel aug-2021
        #
        # IMPORTANT: ensure that this entry_points coincides with that of edx-platform
        #            and also that you are not introducing any name collisions.
        # https://github.com/openedx/edx-platform/blob/master/setup.py#L88
        "lms.djangoapp": [
            "memberpress_client = memberpress_client.apps:MemberPressPluginConfig",
        ],
        "cms.djangoapp": [],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
