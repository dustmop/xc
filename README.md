## xc

A tiny command-line calculator for mixed decimal / hexadecimal math. It is focused on ease of use and convenience.

# Install

```
pip install xc
```

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

```
> xc -x '123 * 345'

a5c3
```

# Flags

`-x` Only output hexadecimal (with no prefix)

`-d` Only output decimal

# Supported

`+`, `-` : addition, subtraction

`*`, `/` : multiplication, division (make sure to escape `*` on the command-line)

`**` : exponentiation

`0x12` : hexadecimal numbers

`-0x34` : negative hexadecimal numbers, displayed as unsigned values
