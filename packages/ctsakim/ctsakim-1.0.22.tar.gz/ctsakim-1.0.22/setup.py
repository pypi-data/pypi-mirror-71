from setuptools import setup

setup(name='ctsakim',
      version='1.0.22',
      description='Cts akim okuma',
      url='https://gitlab.com/ctsyazilim/ctsakim.git',
      author='Soner Akarsu',
      author_email='soner.akarsu@cts.com.tr',
      license='MIT',
      packages = ['ctsakim'],
      scripts=['ctsakim/ctsakim.py'],
      install_requires=[
          'Adafruit-MCP3008'
      ],
      zip_safe=False)