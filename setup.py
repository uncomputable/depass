from setuptools import setup

setup(
    name="depass",
    version="0.1",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "depass=main:main",
        ],
    },
)
