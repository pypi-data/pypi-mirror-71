# Binary Quiz

## Description

A command line application and Python library for generating binary numbers for a human to decode, as well as generating the integers they represent, to check the human's work.

## Compatibility

Currently only supported on MacOS and Linux

## Installation on MacOS or Linux
1) `brew install ghostscript` ([install homebrew](https://brew.sh) if needed)
2) `brew install enscript`
3) `pip install binary-quiz`

## Usage
```
binary [OPTIONS] BITS NUM_PROBLEMS

Options:
  --pdf
  --silent
  --include-answers
  --output-filepath TEXT
  --help                  Show this message and exit.

```

## Examples of Output

### PDF

```shell
$ binary 8 100 --pdf
```

👆👆 this command produces two PDFs like this 👇👇

[![example of problems.pdf output](https://github.com/zevaverbach/binary_quiz/blob/master/examples/problems.png)](https://github.com/zevaverbach/binary_quiz/blob/master/examples/problems.pdf)
[![example of problems-answers.pdf output](https://github.com/zevaverbach/binary_quiz/blob/master/examples/problems-answers.png)](https://github.com/zevaverbach/binary_quiz/blob/master/examples/problems-answers.pdf)

### stdout

```shell
00011110

00111000

11101000

11110000

01011101

01100110

01010010

01110010

10101001

10001010

10010010

11111101

10001110

01111111

00001110

11101011

00010011

00101000

01011010

01001001

01011101

11000011

10000000

11011001

10000110

00000101

11110100

11000010

00110000

11010110

10100101

01000100

00011000

11111111

00111100

00010010

01101111

10101001

10001011

00011011

11010011

01001000

01011111

01010101

10111011

11100010

10011010

10011110

11000010

10001110

11100101

11000101

01001001

01100010

10010001

01110110

11000100

11101101

10000111

10010111

10111100

01001111

10001001

00111001

10001011

10110110

10001001

10100100

01110000

01110001

01111100

10001101

00010000

11001110

01011010

01110000

10000101

01110001

10100110

01010001

00100100

11011011

00011000

11010110

01000001

00111101

11010010

01001110

01100001

10100100

10110100

01000000

00100010

01101010

10000001

11111100

10010011

11001011

11001010

01011100
*BEGIN ANSWERS*
00011110 | 30 

00111000 | 56 

11101000 | 232 

11110000 | 240 

01011101 | 93 

01100110 | 102 

01010010 | 82 

01110010 | 114 

10101001 | 169 

10001010 | 138 

10010010 | 146 

11111101 | 253 

10001110 | 142 

01111111 | 127 

00001110 | 14 

11101011 | 235 

00010011 | 19 

00101000 | 40 

01011010 | 90 

01001001 | 73 

01011101 | 93 

11000011 | 195 

10000000 | 128 

11011001 | 217 

10000110 | 134 

00000101 | 5 

11110100 | 244 

11000010 | 194 

00110000 | 48 

11010110 | 214 

10100101 | 165 

01000100 | 68 

00011000 | 24 

11111111 | 255 

00111100 | 60 

00010010 | 18 

01101111 | 111 

10101001 | 169 

10001011 | 139 

00011011 | 27 

11010011 | 211 

01001000 | 72 

01011111 | 95 

01010101 | 85 

10111011 | 187 

11100010 | 226 

10011010 | 154 

10011110 | 158 

11000010 | 194 

10001110 | 142 

11100101 | 229 

11000101 | 197 

01001001 | 73 

01100010 | 98 

10010001 | 145 

01110110 | 118 

11000100 | 196 

11101101 | 237 

10000111 | 135 

10010111 | 151 

10111100 | 188 

01001111 | 79 

10001001 | 137 

00111001 | 57 

10001011 | 139 

10110110 | 182 

10001001 | 137 

10100100 | 164 

01110000 | 112 

01110001 | 113 

01111100 | 124 

10001101 | 141 

00010000 | 16 

11001110 | 206 

01011010 | 90 

01110000 | 112 

10000101 | 133 

01110001 | 113 

10100110 | 166 

01010001 | 81 

00100100 | 36 

11011011 | 219 

00011000 | 24 

11010110 | 214 

01000001 | 65 

00111101 | 61 

11010010 | 210 

01001110 | 78 

01100001 | 97 

10100100 | 164 

10110100 | 180 

01000000 | 64 

00100010 | 34 

01101010 | 106 

10000001 | 129 

11111100 | 252 

10010011 | 147 

11001011 | 203 

11001010 | 202 

01011100 | 92 

```

## Other Projects That Could Be Built Using This Package
- do the problems online/on computer
- a website to serve these up and let people use them for free
  - a web API that serves it, so people can do that programmatically
  - a snail mail service?
    - https://developers.lulu.com/price-calculator
  - if there's going to be exercises in the browser,
    - parseInt('0101', 2)
  - maybe re-implement in Javascript so all computation and rendering is done on the client
    - [PDF rendering in the browser](https://pspdfkit.com/blog/2018/render-pdfs-in-the-browser-with-pdf-js/)
