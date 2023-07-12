from setuptools import setup, find_packages

setup(name="mess_clientVAG",
      version="0.0.1",
      description="mess_clientVAG",
      author="Ganenko Vladislav",
      author_email="vladislavchicheg@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
