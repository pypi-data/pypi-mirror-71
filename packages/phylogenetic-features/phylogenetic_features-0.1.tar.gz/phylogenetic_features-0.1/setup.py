import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name='phylogenetic_features',

    version='0.1',

    author="Domingos Dias",

    author_email="domingos.adj@nca.ufma.br",

    description="A package to extract phylogenetic features",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/Dowingows/phylogenetic_features",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

    ],

)
