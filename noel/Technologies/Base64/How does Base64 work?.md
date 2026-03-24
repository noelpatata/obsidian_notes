## Why Base64 exists

Binary data (images, executables, encrypted blobs) contains bytes from 0x00 to 0xFF. Many protocols (email, JSON, URLs) only handle printable ASCII text safely. Base64 converts arbitrary binary into a safe 64-character alphabet so it can travel through text-only channels without corruption.

## The Alphabet

Base64 uses exactly 64 characters, each representing a 6-bit value (2⁶ = 64):

```
Index  Char    Index  Char    Index  Char    Index  Char
─────  ────    ─────  ────    ─────  ────    ─────  ────
  0      A       16     Q       32     g       48     w
  1      B       17     R       33     h       49     x
  2      C       18     S       34     i       50     y
  3      D       19     T       35     j       51     z
  4      E       20     U       36     k       52     0
  5      F       21     V       37     l       53     1
  6      G       22     W       38     m       54     2
  7      H       23     X       39     n       55     3
  8      I       24     Y       40     o       56     4
  9      J       25     Z       41     p       57     5
 10      K       26     a       42     q       58     6
 11      L       27     b       43     r       59     7
 12      M       28     c       44     s       60     8
 13      N       29     d       45     t       61     9
 14      O       30     e       46     u       62     +
 15      P       31     f       47     v       63     /
```

Plus `=` as a padding character.

## The Core Idea

**8-bit bytes → 6-bit groups**

Computers store data in 8-bit bytes, but Base64 works in 6-bit groups. The trick is finding a common multiple: LCM(8, 6) = 24 bits = 3 bytes = 4 Base64 characters.

```
3 bytes input  →  4 characters output  (33% size increase)
```

## Encoding Step by Step

### Example: Encoding "Man"

**Step 1 — Get the ASCII values:**

```
'M' = 77    'a' = 97    'n' = 110
```

**Step 2 — Convert to binary (8 bits each):**

```
M:  0 1 0 0 1 1 0 1
a:  0 1 1 0 0 0 0 1
n:  0 1 1 0 1 1 1 0
```

**Step 3 — Concatenate all 24 bits:**

```
0 1 0 0 1 1 0 1 | 0 1 1 0 0 0 0 1 | 0 1 1 0 1 1 1 0
```

**Step 4 — Regroup into 6-bit chunks:**

```
0 1 0 0 1 1 | 0 1 0 1 1 0 | 0 0 0 1 0 1 | 1 0 1 1 1 0
─────────────  ─────────────  ─────────────  ─────────────
    19              22              5              46
```

**Step 5 — Map each 6-bit value to the Base64 alphabet:**

```
19 → T     22 → W     5 → F     46 → u
```

**Result:** `"Man"` → `"TWFu"`

## The Bit Manipulation (What the Code Does)

Given 3 bytes `b0`, `b1`, `b2`:

```c
// Pack into a 24-bit integer
unsigned int triple = (b0 << 16) | (b1 << 8) | b2;

// Extract 4 groups of 6 bits
char c0 = table[(triple >> 18) & 0x3F];  // bits 23-18
char c1 = table[(triple >> 12) & 0x3F];  // bits 17-12
char c2 = table[(triple >>  6) & 0x3F];  // bits 11-6
char c3 = table[(triple >>  0) & 0x3F];  // bits  5-0
```

Why `0x3F`? It's `00111111` in binary — a mask that keeps only the lowest 6 bits.

Visually:

```
         b0              b1              b2
  ┌───────────────┬───────────────┬───────────────┐
  │7 6 5 4 3 2 1 0│7 6 5 4 3 2 1 0│7 6 5 4 3 2 1 0│  ← 8-bit groups
  └───────────────┴───────────────┴───────────────┘
  ┌───────────┬───────────┬───────────┬───────────┐
  │5 4 3 2 1 0│5 4 3 2 1 0│5 4 3 2 1 0│5 4 3 2 1 0│  ← 6-bit groups
  └───────────┴───────────┴───────────┴───────────┘
      c0           c1           c2           c3
```

## Padding: When Input Isn't Divisible by 3

Base64 works in groups of 3 bytes. If the input length isn't a multiple of 3, we pad:

### 1 byte remaining (e.g. "A")

```
'A' = 65 = 01000001

Split into 6-bit groups (only 8 bits available, pad with zeros):
  010000 | 01‹0000›          ← 4 zero bits added
     Q        Q

Output: QQ==                 ← two '=' padding characters
```

The two `=` tell the decoder: "only 1 real byte here, ignore the last 2."

### 2 bytes remaining (e.g. "AB")

```
'A' = 01000001    'B' = 01000010

Split 16 bits into 6-bit groups (pad with zeros):
  010000 | 010100 | 0010‹00›    ← 2 zero bits added
     Q       U       I

Output: QUI=                     ← one '=' padding character
```

The one `=` tells the decoder: "only 2 real bytes here, ignore the last 1."

### Summary

|Input bytes|Output chars|Padding|
|---|---|---|
|3|4|none|
|2|3 + `=`|1|
|1|2 + `==`|2|

## Decoding (The Reverse)

Decoding is the exact reverse:

1. Take 4 Base64 characters
2. Map each to its 6-bit value using the reverse lookup table
3. Combine into a 24-bit integer
4. Extract 3 bytes

```c
unsigned int triple = (v0 << 18) | (v1 << 12) | (v2 << 6) | v3;

unsigned char byte0 = (triple >> 16) & 0xFF;
unsigned char byte1 = (triple >>  8) & 0xFF;
unsigned char byte2 = (triple >>  0) & 0xFF;
```

If the input ends with `=`, skip the corresponding output bytes.

## Size Overhead

Every 3 bytes become 4 characters: a **33% increase** in size. This is the cost of making binary data text-safe.

```
Original size:  n bytes
Encoded size:   ⌈n/3⌉ × 4 characters
```

## Where You See Base64

- **Email attachments** (MIME encoding)
- **Data URIs** in HTML/CSS (`data:image/png;base64,iVBOR...`)
- **JWT tokens** (Header.Payload.Signature, each part is Base64URL)
- **HTTP Basic Auth** (`Authorization: Basic dXNlcjpwYXNz`)
- **Embedding binary in JSON/XML**
- **PEM certificates** (the text between `-----BEGIN CERTIFICATE-----`)

## Base64 ≠ Encryption

Base64 is **encoding**, not encryption. It provides zero security — anyone can decode it. It's purely a format conversion for transport compatibility.