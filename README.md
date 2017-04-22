## compileShellCode.py

CompileShellCode.py enables you to embed ~~up to ~65,535 bytes of~~ x86 shellcode into a Windows executable and then execute it. It was built to solve the problems associated with analyzing injected malware that is composed solely of posistion independent code. In the past I would load and execute my shellcode from a seperate file, but setting breakpoints and saving comments for shellcode executed in this way gets pretty frustrating in Ida Pro in my opinion.

In this program shellcode is read from a file, converted into a resource, and then compiled into an executable that will search for the shellcode and then set the shellcode as executable using VirtualProtect so you can easily set breakpoints within the finished executable. It also disables ASLR and sets the preferred load address of the executable. 

## Files:

compileShellCode.py - Reads the shellcode file, sets up everything needed by the compiler, and runs the compiler
cppcode.py - C++ source code template that makes up the finished executable
resource.h - Header file which defines the resource definitions
shellcode.rc - Contains the resource script used by the resource compiler (rc.exe)

## Usage

This program must be run from the Visual Studio command line as it relies on cl.exe to compile the C++, and currently it only supports x86 for Windows. In the future I will add x64 support. Make sure to check the load resourses box in Ida Pro when you load the exe. You can easily find the shellcode by going to the resource section or searching for the Unicode string SHELLCODE.

```
usage: compileShellCode.py [-h] -s SHELLCODEPATH -o OUTFILENAME

Creates an exe with shellcode embedded as a resource. Must be run from Visual
Studio developer's command prompt.

optional arguments:
  -h, --help            show this help message and exit
  -s SHELLCODEPATH, --shellCodePath SHELLCODEPATH
                        Path to shell code.
  -o OUTFILENAME, --outFileName OUTFILENAME
                        Output filename with no extension

ex: python compileShellCode.py -s myShellcode -o out
```

