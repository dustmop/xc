## xc

A simple command-line calculator for mixed decimal / hexidecimal math.

# Examples

```
> xc 12

0xc   12
```

```
> xc 10 0x10 100 0x100

0x00a    10
0x010    16
0x064   100
0x100   256
```

```
> xc 0x40 + 20

0x54   84
```

```
> xc -0x21 \* 5

0xff5b   -165
```

# Install

```
alias xc=`python xc.py`
```
