[BACK](../README.md)
# Programming

### Python:
- If the input is a number:
  - Try passing inf,-inf or NaN
    - ex: 1 + NaN = NaN
- To get info about a function:
  - print(func.__code__)
  - the code has useful attributes like co_consts, co_varnames, co_names, co_code
    - co_consts: tuple of constants used in the function
    - co_varnames: tuple of variable names
    - co_names: tuple of names used in the function
    - co_code: bytecode of the function
- Can leak data with format string vulnerabilities
  - ex: username = "{}".format(user_input)
  - user_input = "__init__.__globals__[sercret_key]"
- Mutable variables
  - If a mutable variable is used as a default argument, it will be shared between all calls to the function
    - ex: def f(a=[]): a.append(1); return a
    - f() -> [1]
    - f() -> [1,1]
    - f() -> [1,1,1]
  - To avoid this, use None as the default argument and set the default value inside the function
    - ex: def f(a=None): if a is None: a = []; a.append(1); return a
- Quick template:
  - ().__class__.__bases__[0].__subclasses__()[INDEX_OF_POPEN](["/bin/cat","flag"], stdout=-1).communicate()
### Python 2
- `input()` is equivalent to `eval(raw_input())`
- func_code is used instead of __code__
  
### PHP:
- PHP supports loose comparaison
  - If a string starts with 0e and is followed only by numbers, it is equal to 0, or 1e = 1
    - Considered as scientific notation. 0^numbers = 0 and 1^numbers = 1
- https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Type%20Juggling/README.md

### GuptaLang

#### [Doc](https://samples.tdcommunity.net/samples/TDMobile/Documents/OpenText%20Gupta%20TD%20Mobile%20Primer.pdf)

- Functions starting with "Sal"
  - ex: SalStrLength(str)
- || is used to append strings

### Perl
- if using open with 2 arguments instead of 3:
  - Can do command injection
  - ex: `open(F, $user_input)` -> We can pass: `| cat .passwd`

### PowerShell

- If iex(Invoke-Expression aka eval) is used:
  - Can use command injection 
  
#### Convert SecureString to plain text
```powershell
[System.Net.NetworkCredential]::new("", $SecurePassword).Password
```


### C/C++

- mblen:
  - Returns the number of bytes in the next multibyte character
  - If the next character is a null byte, it returns 0
  - If the next character is not a valid multibyte character, it returns -1
  ANSI = chars 0-255; ASCII = chars 0-127
- htons() -> Takes 16 bit number in the host os byte order (big/little endian) and returns the value in TCP/IP byte order
- HWND -> Window Handle
- LPCSTR -> 32 bit ptr to a constant string of ANSI chars (LP = Long pointer)

### Rust
- Cargo can execute code at build time if a build.rs file is present
  - Can be used to run arbitrary code

### Ruby
- Can concatenate strings using << operator with bytes
  - ex: "" << 65 << 66 << 67 -> "ABC"
- Can create empty string using eval(%%%)
- same with %<>
- eval("$*<<$0;p *$<")
  - Read the content of the running file and print it 