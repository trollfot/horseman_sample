import os
from setuptools import setup, find_packages


version = "0.1"

install_requires = [
    'bjoern',
    'chameleon',
    'horseman',
]


test_requires = [
]


setup(
    name='sample',
    version=version,
    author='Souheil Chelfouh',
    author_email='contact@example.com',
    url='http://www.example.com',
    download_url='',
    description='Sample Horseman Application',
    long_description=(open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read()),
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python:: 3 :: Only',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
    entry_points={
    }
)
