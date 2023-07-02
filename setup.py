from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in cash_holder_summary/__init__.py
from cash_holder_summary import __version__ as version

setup(
	name="cash_holder_summary",
	version=version,
	description="Summary of payments for a cash holder account for a given period",
	author="Kitti U.",
	author_email="kittiu@flo-works.co",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
