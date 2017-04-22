import cppcode
import subprocess
import os
import argparse

def getByteString(fileName):
    '''
    Makes a byte array and gets length from file containing shellcode.

    Reads a specified file of shellcode, gets the length of the shellcode,
    then adds the little endiam marker used to find the shellcode when the
    exe is run.

    Returns:
        The shellcode with the marker added, and the length of the shellcode
    '''
    with open(fileName, "rb") as f:
        blob = bytearray(f.read())
    lenShellcode = len(blob)
    marker = "\xFF\xFF\xFF\xFF\xEF\xBE\xAD\xDE"
    return marker + blob, lenShellcode

def copyToResource(shellcode):
    '''
    Rewrites the shellcode to be used by the .rc file

    Really this is just writing the shellcode with marker
    to disk and adding .bin to it. if you want to change the filename
    used here you must also change it in the .rc file
    Args:
       Shellcode with marker
    '''

    with open("shellcode.bin", "wb") as f:
        f.write(shellcode)


def writeCpp(lenShellcode, outCppFileName):
    '''
    Writes the formatted shellcode string to the output .cpp file.

    Args:
        The shellcode string, the length of the Shellcode, and the
        .cpp output filename.
    Returns:
        nothing
    '''
    outCppFileName += ".cpp"
    sourceCode = cppcode.code
    sourceWithShellCode = sourceCode.format(lenShellcode)
    print "wrote :", outCppFileName
    with open(outCppFileName, "wb") as f:
        f.write(sourceWithShellCode)

def setupResource():
    '''
    Runs the MS resource compiler on shellcode.rc, creates shellcode.res

    '''

    subprocess.call(["rc.exe","shellcode.rc"])

def compileExe(outCppFileName):
    '''
    Compiles the C++ source code with resource file

    Overwrites the output exe if it already exists, and then removes the exe
    extension for safety. I set the base and disabled aslr to hopefully allow
    the exe to load at the same memory address each time.

    Args:
        Output filename with no file extension
    '''
    out = outCppFileName
    outCppName = out + ".cpp"
    outExeName = out + ".exe"
    outExeSafeName = outExeName + "_"
    print("\nCompiling...")
    try:
        subprocess.call(["cl.exe",
                         "/sdl",
                         "/EHsc",
                         outCppName,
                         "/link",
                         "/base:0x800000",
                         "/DYNAMICBASE:NO",
                         "shellcode.res",])
        outExeName = outCppFileName + ".exe"

        print("\nCompiler finished")
        try:
            os.rename(outExeName, outExeSafeName)
        except:
            os.remove(outExeSafeName)
            print("The file {0} already exists, overwriting the old copy.".format(outExeSafeName))
            os.rename(outExeName, outExeSafeName)

        print("Added a '_' to the executable name.")
        print("Successfully created an exe with shellcode")
    except Exception as e:
        print("Something went wrong while compiling.")
        print(e)


def main():
    desc = '''Creates an exe with shellcode embedded as a resource.
              Must be run from Visual Studio developer's command prompt.'''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s',
                        '--shellCodePath',
                        action='store',
                        required=True,
                        help="Path to shell code.")
    parser.add_argument('-o',
                        '--outFileName',
                        action='store',
                        required=True,
                        help="Output filename with no extension")
    args = parser.parse_args()

    shellcode, lenShellcode = getByteString(args.shellCodePath)
    copyToResource(shellcode)
    setupResource()
    writeCpp(lenShellcode, args.outFileName)
    compileExe(args.outFileName)

if __name__ == '__main__':
    main()
