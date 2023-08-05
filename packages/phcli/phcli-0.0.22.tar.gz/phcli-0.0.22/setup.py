import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phcli",
    version="0.0.22",
    author="Alfred Yang",
    author_email="alfredyang@pharbers.com",
    description="pharbers dag scheduler config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',

    package_data={
        '': ['template/*.yaml', 'template/*.tmp']
    },
    entry_points={
        'console_scripts': [
            'phcli = command.phcommand:ph_command',
        ],
    }
)
