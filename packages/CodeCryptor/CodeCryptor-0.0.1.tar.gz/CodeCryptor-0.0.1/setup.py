from setuptools import setup, find_packages
setup(
    name="CodeCryptor",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
          'console_scripts': [
              'CodeCryptor = CodeCryptor.__main__:main'
          ]
      },

    install_requires=["PyNaCl>=1.4.0"],

    # metadata to display on PyPI
    author="John Alejandro González",
    author_email="johnalejandrog.g4@gmail.com",
    description="A Python Module for the encryption of code modules",
    keywords="encryption crypto decryption python code security",
    url="https://github.com/KurtCoVayne/CodeCryptor", 
    project_urls={
        "Bug Tracker": "https://github.com/KurtCoVayne/CodeCryptor",
        "Documentation": "https://github.com/KurtCoVayne/CodeCryptor/",
        "Source Code": "https://github.com/KurtCoVayne/CodeCryptor",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

)