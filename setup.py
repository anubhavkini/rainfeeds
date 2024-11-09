from setuptools import setup, find_packages

setup(
    name="raindrop",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "datetime",
        "feedparser",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "rainfeeds=src.main:main"
        ]
    }
)
