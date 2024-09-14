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
