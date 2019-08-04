import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
	name='algebra',
	version='0.1',
	description="Abstract Algebra in Python",
	long_description=long_description,
	long_description_content_type='text/markdown',
	url="https://github.com/kayvontabrizi/abstract-algebra",
	packages=setuptools.find_packages(),
)
