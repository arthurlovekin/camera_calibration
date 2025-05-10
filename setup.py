from setuptools import setup, find_packages

setup(
    name="camera_calibration",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.4",
        "numpy>=1.19.0",
    ],
    python_requires=">=3.7",
    author="Arthur",
    description="A concise package for intrinsic and extrinsic camera calibration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "camera-calibration=camera_calibration.main:main",
        ],
    },
) 