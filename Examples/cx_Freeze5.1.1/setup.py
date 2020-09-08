from cx_Freeze import setup, Executable

setup(name = "hello_world",
      version = "0.1",
	  description = "test build",
      executables = [Executable("hello_world.py")]
	  )