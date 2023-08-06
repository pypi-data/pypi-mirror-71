from setuptools import find_packages, setup

setup(
  name = 'FreeTAKServer',         # How you named your package folder (MyLib)
  packages = ['FreeTAKServer', 'FreeTAKServer.controllers', 'FreeTAKServer.controllers.constants', 'FreeTAKServer.controllers.model'],   # Chose the same as "name"
  version = '0.8.13',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'Ghosty 1008',                   # Type in your name
  author_email = 'your.email@domain.com',      # Type in your E-Mail
  url = 'https://github.com/naman108/FreeTAKServerPip',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/naman108/FreeTAKServerPip/archive/0.8.7.tar.gz',    # I explain this later on
  keywords = ['TAK', 'OPENSOURCE'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'flask',
          'lxml',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)