from setuptools import setup

setup(name='bepy',
      version='1.0.0',
      description="A framework for materials characterization data collected that facilitates post analysis",
      url='https://github.com/lgriffin39/bepy',
      author='Lee Griffin',
      author_email='lgriffin39@gatech.edu',
      license='MIT',
      packages=['bepy'],
      install_requires=['numpy', 'pandas', 'matplotlib', 'scipy'],
      zip_safe=False)
