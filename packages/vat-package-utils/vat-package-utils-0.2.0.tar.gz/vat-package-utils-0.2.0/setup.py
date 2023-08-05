"""
setup.py
"""

from setuptools import find_packages, setup

###

NAME = 'vat-package-utils'
VERSION = '0.2.0'
PACKAGES = find_packages(where='src')
INSTALL_REQUIRES = [
    'boto3'
]
SCRIPTS = [
    'vat_publish_packages = vat_package_utils.publish_packages:main'
]

AUTHOR = 'VAT Dev'
AUTHOR_EMAIL = 'vatdev@invalid.in'

###

if __name__ == '__main__':
    setup(
        name=NAME,
        version=VERSION,
        packages=PACKAGES,
        package_dir={"": "src"},
        entry_points={
            'console_scripts': SCRIPTS
        },
        install_requires=INSTALL_REQUIRES,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL
    )
