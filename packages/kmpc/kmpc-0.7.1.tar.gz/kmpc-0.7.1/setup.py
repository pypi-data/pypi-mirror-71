from setuptools import setup

from kmpc.version import VERSION, VERSION_STR

setup(
    version=VERSION_STR,
    download_url='https://gitlab.com/eratosthene/kmpc/archive/'
                 + VERSION_STR
                 + '.tar.gz',
    setup_requires=['setuptools>=38.4.0'],
    setup_cfg=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2.7',
    ],
)
