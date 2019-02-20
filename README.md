## xc

A tiny command-line calculator for mixed decimal / hexidecimal math.

# Examples

```
> xc 0x40 + 20

0x54   84
```

```
> xc 10 0x10 100 0x100

0x00a    10
0x010    16
0x064   100
0x100   256
```

```
> xc -0x21 \* 5

0xff5b   -165
```

# Supported:

`+`, `-` : addition, subtraction

`*`, `/` : multiplication, division (make sure to escape `*` on the command-line)

`**` : exponentiation

`0x12` : hexidecimal numbers

`-0x34` : negative hexidecimal numbers, displayed as unsigned values

# Install

```
alias xc=`python xc.py`
```
