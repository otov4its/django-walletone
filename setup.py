import os.path
from setuptools import setup, find_packages
from walletone import __version__


def long_description():
    here = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(here, 'README.rst')).read()


setup(
    name="django-walletone",
    version=__version__,
    description='WalletOne payment system integration in Django.',
    long_description=long_description(),
    url='https://github.com/otov4its/django-walletone',
    license='MIT',
    author='Stanislav Otovchits',
    author_email='otov4its@gmail.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'Django>=1.7'
    ],
    keywords=['django', 'walletone', 'w1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
