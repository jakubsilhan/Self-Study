# Summary
A document for practice of grammar creation

# Integer
## First try - not optimal
```
int = '0' | nz_digit;
nz_digit = ('1' | '...' | '9'), {digit};
digit = '0', {digit} | nz_digit;
```
## Second try - optimal
```
int = '0' | nz_digit;
nz_digit = ('1' | '...' | '9'), {digit};
digit = '0'|...|'9';
```

# Float
- adding operators + and -
- adding decimal separator
```
double = operator,number | number | '0';
operator = '+' | '-';
number = float| integer;
float = '0','.',{digit}|nz_digit, '.', {digit};
integer = nz_digit;
nz_digit = ('1' | '...' | '9'), {digit};
digit = '0'|'...'|'9';
```

# Hexadecimal
```
hexa = '0x' {digit}
digit = "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"A"|"B"|"C"|"D"|"E"|"F"|"a"|"b"|"c"|"d"|"e"|"f"
```

# Function
```
function = fun_identifier '=' '(' [params] ')'
params = param_identifier {',' param_identifier}
param_identifier = letter{letter}
fun_identifier = letter{letter}
letter = "A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N"
       | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
       | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
       | "c" | "d" | "e" | "f" | "g" | "h" | "i"
       | "j" | "k" | "l" | "m" | "n" | "o" | "p"
       | "q" | "r" | "s" | "t" | "u" | "v" | "w"
       | "x" | "y" | "z" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "_"
```

# Expression
```
v = v,"+",v | v,"*",v | "(",v,")" | "a"
```

# Assignment
```
expression = identifier,"=",v
v = v,"+",v | v,"*",v | "(",v,")" | "a" 
identifier = letter{letter}
letter = "A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N"
       | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
       | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
       | "c" | "d" | "e" | "f" | "g" | "h" | "i"
       | "j" | "k" | "l" | "m" | "n" | "o" | "p"
       | "q" | "r" | "s" | "t" | "u" | "v" | "w"
       | "x" | "y" | "z" | "0" | "1" | "2" | "3"
       | "4" | "5" | "6" | "7" | "8" | "9" | "_"
```
