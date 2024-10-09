from setuptools import find_packages
from numpy.distutils.core import setup


setup(
    name='TraitTrackerSolver',
    version='0.1',
    description='Tool to compute and analyse TFT set 12 compositions',
    url='https://github.com/benjabern/TraitTrackerSolver',
    python_requires=">=3.8",
    packages=find_packages(include=['tts']),
    install_requires=['numpy', 'tqdm'],
    include_package_data=True,
    package_data={"tts.data": ["*.npy"]},
    entry_points={
    'console_scripts': [
        'tts = tts.main:main'
            ]
    },

)