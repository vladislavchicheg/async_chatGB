import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["common", "log", "server", "unit_tests"],
}
setup(
    name="mess_serverVAG",
    version="0.0.1",
    description="mess_serverVAG",
    options={
        "build_exe": build_exe_options
    },
    executables=[Executable('server.py',
                            # base='Win32GUI',

                            )]
)
