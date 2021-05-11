import os
from setuptools import setup
from pathlib import Path

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
HOME_DIRECTORY = str(Path.home())


setup(name='simple_smtp_client',
      version='1.0',
      description='Simple SMTP client.',
      author='Vladyslav Barbanyagra',
      author_email='mrcontego@gmail.com',
      install_requires=open(os.path.join(CURRENT_DIRECTORY, 'requirements.txt')).readlines(),
      entry_points={
            'console_scripts': ['simple_smtp_client=main.runner:main'],
      },
      packages=['main'],
      data_files=[(('simple_smtp_client_resources'), ['resources/config.ini'])])
