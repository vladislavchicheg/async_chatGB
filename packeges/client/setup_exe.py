import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["common", "log", "client", "unit_tests"],
}
setup(
    name="mess_clientVAG",
    version="0.0.1",
    description="mess_clientVAG",
    options={
        "build_exe": build_exe_options
    },
    executables=[Executable('client.py',
                            # base='Win32GUI',

                            )]
)
