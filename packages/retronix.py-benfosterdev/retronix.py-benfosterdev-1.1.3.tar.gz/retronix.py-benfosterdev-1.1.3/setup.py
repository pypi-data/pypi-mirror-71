#!/usr/bin/env python

import setuptools as st

if __name__ == "__main__":
    
    # It's bug hunting time

    with open("README.md", "r") as f:
        ld = f.read()

    st.setup(
        name="retronix.py-benfosterdev",
        version="1.1.3",
        author="Ben Foster",
        author_email="ben@benfoster.dev",

        description="A Python library for the interaction with the Retronix public API",
        long_description=ld,
        long_description_content_type="text/markdown",

        url="https://github.com/retronixmc/retronix.py",

        packages=st.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
        
        python_requires='>=3.7'
    )
