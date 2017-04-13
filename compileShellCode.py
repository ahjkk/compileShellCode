import cppcode
import subprocess
import os
import argparse


def getByteString(fileName):
    '''
    Makes a byte array and gets length from file containing shellcode.

    Reads a specified file of shellcode, gets the length of the shellcode
    and then passes the shellcode byte array to sliceByteArray where
    the shellcode is cut into 2048 byte chunks. The list of slices is then
    sent to joinSlices where it is joined into  C++ byte strings which are
    2048 bytes long.

    Returns:
        A formated string of bytes that will be inserted into the .cpp file
        used to compile the shellcode into an exe, and the length of the
        shellcode.
    '''
    with open(fileName, "rb") as f:
        blob = bytearray(f.read())
    lenShellcode = len(blob)
    slices = sliceByteArray(blob)
    bString = joinSlices(slices)
    return bString, lenShellcode


def sliceByteArray(bArray):
    '''
    Slices the byte array of shellcode into chunks of 2048 bytes.

    This is to get around the max string size in visual studio.

    Args:
        A bytearray of shellcode
    Returns:
        A list of 2048 byte chunks of shellcode
    '''
    maxStringSize = 2048
    sliced = [bArray[i:i + maxStringSize] for i in xrange(0, len(bArray), maxStringSize)]
    return sliced


def joinSlices(slices):
    '''
    converts a byte array into to a C\C++ byte string

    Adds quotes, tab indentation and new line characters so the byte strings
    are formatted correctly in the .cpp outputfile. Marker is used by the cpp
    program to find the beginning of the shellcode and must be in little
    endian.

    Args:
        A list of of bytearrays
    Returns:
        A C++ formatted string of bytes
    '''
    joinedSlices = ["\\x".join("{:02x}".format(b) for b in s) for s in slices]
    formattedSlices = ['\t"\\x' + slice + '"\r' for slice in joinedSlices]
    marker = '"\\xFF\\xFF\\xFF\\xFF\\xEF\\xBE\\xAD\\xDE"\r'
    return marker + ''.join(formattedSlices).rstrip()


def writeCpp(shellcode, lenShellcode, outCppFileName):
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
    sourceWithShellCode = sourceCode.format(shellcode, lenShellcode)
    print "wrote :", outCppFileName
    with open(outCppFileName, "wb") as f:
        f.write(sourceWithShellCode)


def compileExe(outCppFileName):
    '''
    Compiles the C++ source code

    Overwrites the output exe if it already exists, and then removes the exe
    extension for safety. I set the base and disabled aslr to hopefully allow
    the exe to load at the same memory address each time. I wanted
    to have the shellcode at a offset ending in 0x00000 but it looks like
    this is not possible with this linker as it requires that the base be
    64KB aligned and ending in four zeros. Can rebase the program in ida
    if necessary.

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
                         "/DYNAMICBASE:NO"])
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
    desc = '''Inserts up to 65,535 bytes of shellcode into a .cpp file and then compiles it.
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
    if lenShellcode < 65535:
        writeCpp(shellcode, lenShellcode, args.outFileName)
        compileExe(args.outFileName)
    else:
        # 65535 is the maximum size of a string in visual studio
        print("Sorry the file size to embed must be less than 65535")


if __name__ == '__main__':
    main()
