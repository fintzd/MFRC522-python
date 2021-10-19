from setuptools import setup, find_packages


VERSION = "0.0.1"
DESCRIPTION = "Reading and writing RFID tags with python."
LONG_DESCRIPTION = "Python3 library to read & write RFID tags with a physical MFRC522 RFID module and a Raspberry Pi."

setup(
    name="rfid522",
    version=VERSION,
    author="fintzd",
    author_email="fintzd@tuta.io",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/fintzd/MFRC522-python",
    packages=find_packages(),
    install_requires=['RPi.GPIO', 'spidev'],
    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: POSIX :: Linux",
        'Topic :: System :: Hardware',
    ],
)
