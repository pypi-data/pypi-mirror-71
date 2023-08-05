"""Setup file for package."""
import setuptools

with open("README.md", 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
      name='can',
      packages=['can'],
      scripts=[],
      description='A color animator.',
      install_requires=[],
      url='https://github.com/crainiac/can',
      author='Alex Crain',
      author_email='alex@crain.xyz',
      platforms=['any'],
      license='MIT',
      classifiers=[
          'Programming Language :: Python :: 3',
	  'License :: OSI Approved :: MIT License',
	  'Operating System :: OS Independent',
      ],
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
)
