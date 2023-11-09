from setuptools import setup

setup(
    name="depass",
    version="1.0",
    scripts=["depass.py"],
    entry_points={
        "console_scripts": [
            "depass=depass:main",
        ],
    },
)
