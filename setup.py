import setuptools


setuptools.setup(
    name="rfid522",
    version="0.0.1",
    author="fintzd",
    author_email="fintzd@tuta.io",
    description="Python3 library to read/write RFID tags via the MFRC522 RFID module.",
    url="https://github.com/fintzd/MFRC522-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'RPi.GPIO',
        'spidev'
        ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: POSIX :: Linux",
        'Topic :: System :: Hardware',
    ],
)
