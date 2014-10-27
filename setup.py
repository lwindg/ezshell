from setuptools import setup
from ezshell import __version__

NAME = "ezshell"
MODULES = ["ezshell"]
DESCRIPTION = "An easy to use shell library"

URL = "https://github.com/Sanji-IO"

AUTHOR = "Sanji Team"
AUTHOR_EMAIL = "sanji@moxa.com"

setup(name=NAME,
      version=__version__,
      py_modules=MODULES,

      # metadata
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      url=URL,
      license="MOXA",
      zip_safe=False
      )
