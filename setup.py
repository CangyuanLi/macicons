import setuptools

setuptools.setup(
    name="macicons",
    version="0.0.4",
    author="Cangyuan Li",
    author_email="everest229@gmail.com",
    description="CLI utility to change Mac Icons.",
    url="https://github.com/CangyuanLi/macicons",
    packages=["macicons"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "macicons=macicons.cli:main"
        ]
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS"
    ]
)