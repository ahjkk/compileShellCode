## compileShellCode.py

CompileShellCode.py enables you to embed ~~up to 65,535 bytes of~~ x86 shellcode into a Windows executable and then execute it. It was built to solve problems associated with analyzing injected malware that is composed solely of posistion independent code. In the past I would load and execute my shellcode from a seperate file, but in Ida Pro this can quickly get frustrating when it comes to saving comments, and the alternative of making segments into loader segments sometimes causes other problems.

In this program shellcode is read from a file, converted into a resource, and then compiled into an executable that will search for the shellcode. Once the shellcoded is found, it's made executable using VirtualProtect so you can easily set breakpoints within the finished executable. ASLR is also disabled and a perferred address is set. 

Previously, I was inserting the shellcode into the template file (cppcode.py), but could only insert up to 65,525 bytes which is the max string size in Visual Studio. Using a resource file eliminates that constraint, but did require adding more resource related files to the project.

## Files

compileShellCode.py - Reads the shellcode file, sets up everything needed by the compiler, and runs the compiler

cppcode.py - C++ source code template that makes up the finished executable

resource.h - Header file which contains the resource definition

shellcode.rc - Contains the resource script used by the resource compiler (rc.exe)

## Usage

This program must be run from the Visual Studio command line as it relies on cl.exe to compile the C++ and rc.exe to compile the resource. Currently it only supports x86 for Windows, but in the future I will add x64 support. Make sure to check the load resources box in Ida Pro when you load the exe. You can easily find the shellcode by going to the resource section or searching for the Unicode string SHELLCODE.

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

