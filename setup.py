""" Setup """
#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = "0.1.0"

setup(
    name="lxnotit",
    version=VERSION,
    description="Simple application for save your personal notes",
    keywords=["notes","pyside"],
    author="Lxpause",
    url="https://github.com/lxpause/lxnotit",
    license="GPL3",
    install_requires=["PySide2>=5.15.2.1"],
    packages=find_packages(),
    python_requires=">=3.5",
    entry_points={
        'console_scripts': [
            'lxnotit=lxnotit.lxnotit:MainWindow.main'
        ]
    },
    include_package_data = True,
    data_files=[
        ( ".",["lxnotit/lxnotitui.py"])
    ]
)
