from setuptools import setup

setup(
    name="depass",
    version="1.0",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "depass=main:main",
        ],
    },
)
