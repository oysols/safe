import setuptools  # type: ignore

setuptools.setup(
    name='safe',
    version='0.1',
    py_modules=["safe"],
    entry_points = {
        'console_scripts': [
            'safe=safe:main',
        ],
    },
    install_requires=["PyNaCl>=1.3.0"],
)
