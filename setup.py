"""Setup script for CheckPCSpecs."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='checkpcspecs',
    version='2.0.0',
    author='apeks827',
    description='A tool to verify if a PC meets minimum system requirements',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/apeks827/CheckPCSpecs',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.9',
    install_requires=[
        'psutil>=5.9.0',
        'py-cpuinfo>=9.0.0',
        'pillow>=10.0.0',
        'speedtest-cli>=2.1.3',
        'icmplib>=3.0.0',
        'requests>=2.31.0',
        'nest-asyncio>=1.5.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'checkpcspecs=checkpcspecs.app:main',
        ],
    },
    package_data={
        'checkpcspecs': ['py.typed'],
    },
    include_package_data=True,
)
