"""
Setup
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="time_series_predictor",
    version="1.0.2",
    author="Daniel Kaminski de Souza",
    author_email="daniel@kryptonunite.com",
    description="Time Series Predictor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://timeseriespredictor.readthedocs.io/",
    packages=['time_series_predictor'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'torch',
        'psutil',
        'tqdm',
        'skorch',
        'scipy'
    ],
    extras_require={
        'dev': [
            'pylint',
            'autopep8',
            'bumpversion',
            'twine',
            'python-dotenv',
            'python-dotenv[cli]',
            'lxml'
        ],
        'test': [
            'pytest',
            'pytest-cov',
            'pandas',
            'seaborn',
            'sklearn'
        ],
        'docs': [
            'sphinx',
            'rstcheck',
            'sphinx-autodoc-typehints',
            'nbsphinx',
            'recommonmark',
            'sphinx_rtd_theme',
            'pandas',
            'seaborn',
            'jupyterlab',
            'matplotlib'
        ]
    }
)
