import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='daigle_dist',
      version="0.1.2",
      author="Christopher Daigle",
      author_email="pcjdaigle@gmail.com",
      description="Gaussian and Binomial Distributions",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ChristopherDaigle/daigle_dist.git",
      packages=['daigle_dist'],
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"],
      python_requires='>=3.6',
      zip_safe=False)
