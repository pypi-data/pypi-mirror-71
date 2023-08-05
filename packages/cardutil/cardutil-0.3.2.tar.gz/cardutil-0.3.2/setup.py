from setuptools import setup, find_packages

readme = open('README.rst', 'r').read()

setup(name='cardutil',
      packages=find_packages(),
      version='0.3.2',
      license='MIT',
      description='Python package for working with payment card systems',
      long_description=readme,
      long_description_content_type='text/x-rst',
      author='Anthony Delosa',
      author_email='adelosa@gmail.com',
      url='https://bitbucket.org/hoganman/cardutil',
      install_requires=[],
      entry_points={
          'console_scripts': [
              'mci_ipm_to_csv = cardutil.cli.mci_ipm_to_csv:cli_entry',
              'mci_csv_to_ipm = cardutil.cli.mci_csv_to_ipm:cli_entry',
              'mci_ipm_encode = cardutil.cli.mci_ipm_encode:cli_entry',
              'mci_ipm_param_encode = cardutil.cli.mci_ipm_param_encode:cli_entry',
          ]
      },
      extras_require={
        'docs': ['sphinx', 'sphinx_rtd_theme', 'cryptography'],
        'test': ['flake8', 'pytest', 'bump2version', 'coverage', 'cryptography'],
        'crypto': ['cryptography']
      },
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
      ])
