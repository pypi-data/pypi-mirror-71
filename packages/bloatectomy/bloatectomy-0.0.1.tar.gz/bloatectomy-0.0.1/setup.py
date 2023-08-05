import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bloatectomy", # Replace with your own username
    version="0.0.1",
    author="Summer Rankin",
    author_email="summerkrankin@gmail.com",
    description="Bloatectomy: a method for the identification and removal of duplicate text in the bloated notes of electronic health records and other documents.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MIT-LCP/mimic-code",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing"
    ],
    python_requires='>=3.7',
)
