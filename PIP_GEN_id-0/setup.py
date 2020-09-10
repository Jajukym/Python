import cx_Freeze
from cx_Freeze import setup, Executable

setup(name = "PIP_Generator",
      version = "21",
      description = "Added arrays to functions",
      executables = [Executable("PIP_GEN_id-0.py")]
      )
