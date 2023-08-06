import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='daniels',
    description='Daniel, the autoreporter.',
    long_description=long_description,
    url="https://github.com/harvested-financial/danielstwine check dist/*",
    version='0.1.6',
    author='Rory Gwozdz',
    author_email='rory@harvestedfinancial.com',
    liscense='MIT',
    packages=setuptools.find_packages(),
    install_requires=['slackclient'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    keywords=['pip', 'slack', 'daniel'],
    python_requires='>=3.6',
)
