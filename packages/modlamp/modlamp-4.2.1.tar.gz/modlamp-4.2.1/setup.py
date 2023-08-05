# -*- coding: utf-8 -*-

from setuptools import setup
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

# parse the requirements from the requirements file
install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs][:-1]

with open('README.rst') as f:
    readme = f.read()

exec(open('modlamp/version.py').read())

setup(name='modlamp',
      version='4.2.1',  # also change version in version.py
      description='python package for in silico peptide design and QSAR studies',
      long_description=readme,
      author='Alex Müller, Gisela Gabernet',
      author_email='alexarnimueller@gmail.com',
      url='http://modlamp.org',
      license='BSD-3',
      keywords="antimicrobial anticancer peptide descriptor sequences QSAR machine learning design",
      packages=['modlamp'],
      package_data={'modlamp': ['data/*.csv', 'data/*.fasta']},
      scripts=['bin/example_modlamp.py', 'bin/example_descriptors.py'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Chemistry',
          'Topic :: Scientific/Engineering :: Medical Science Apps.',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6'],
      install_requires=reqs
      )
