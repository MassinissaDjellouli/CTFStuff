[BACK](../README.md)
# Programming

### Python:
- If the input is a number:
  - Try passing inf,-inf or NaN
    - ex: 1 + NaN = NaN
  
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

### C/C++

- mblen:
  - Returns the number of bytes in the next multibyte character
  - If the next character is a null byte, it returns 0
  - If the next character is not a valid multibyte character, it returns -1
  