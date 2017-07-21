import os
from setuptools import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(name='btctrade',
      version=".".join(map(str, __import__("btctrade").__version__)),
      description='Api for site btc-trade.com.ua/',
      long_description=(read('README.rst')),
      url='http://github.com/FerumFlex/btctrade',
      author='FerumFlex',
      author_email='ferumflex@gmail.com',
      license='MIT',
      packages=['btctrade'],
      install_requires=[
          'requests',
      ],
      classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Operating System :: OS Independent",
            "Topic :: Software Development",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
      ],
      zip_safe=False)