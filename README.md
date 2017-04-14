## compileShellCode.py

CompileShellCode.py enables you to compile up to ~65,535 bytes of x86 shellcode into a Windows executable and then execute it. It was built to solve the problem of analyzing injected malware that is composed solely of shellcode. In the past I would load and execute my shellcode from a seperate file, but setting breakpoints and saving comments for shellcode executed in this way gets pretty frustrating in Ida Pro in my opinion.

In this program shellcode is read from a file as raw bytes, converted into C++ byte strings, and then inserted in to a C++ source code template (cppcode.py) that marks the shellcode as executable using VirtualProtect so you can easily set breakpoints within the finished executable. It also disables ASLR and sets the preferred load address of the executable. 

## Usage

This program must be run from the Visual Studio command line as it relies on cl.exe to compile the C++, and currently it only supports x86 for Windows. In the future I will add x64 and probably support for g++.

```
usage: compileShellCode.py [-h] -s SHELLCODEPATH -o OUTFILENAME

Inserts up to 65,535 bytes of shellcode into a .cpp file and then compiles it.
Must be run from Visual Studio developer's command prompt.

optional arguments:
  -h, --help            show this help message and exit
  -s SHELLCODEPATH, --shellCodePath SHELLCODEPATH
                        Path to shell code.
  -o OUTFILENAME, --outFileName OUTFILENAME
                        Output filename with no extension

ex: python compileShellCode.py -s myShellcode -o out
```

