`https://tryhackme.com/room/breakingcryptothesimpleway`
This challenge of the module `https://tryhackme.com/module/cryptofailures` teaches us the math behind basic RSA public and private keys in order to break them based on given parameters. For example, in this challenge, we have been told to generate the private key based on the following parameters:
Public key = n
Exponent (from public key)= e
Ciphered text (ciphered with private key) = c
## Values
`n = 43941819371451617899582143885098799360907134939870946637129466519309346255747`
`e = 65537`
`c = 9002431156311360251224219512084136121048022631163334079215596223698721862766`

# Procedure
First we need to factor `n` for finding out what `p` and `q`are with the following python script:
``` python
import math  
def getPrimeNumbers(n):  
   prime_numbers = []  
   for num in range(2,n-1):  
       prime = True  
       for i in range(2,num):  
           if ( num % i == 0 ):  
               prime = False  
       if prime:  
           prime_numbers.append(num)  
   return prime_numbers  
  
def factorize_n(n):  
   prime_numbers = getPrimeNumbers(int(math.sqrt(n) + 1))  
   for prime in prime_numbers:  
       if n % prime == 0:  
           p = prime  
           q = n // prime  
           return p, q  
   return None, None
```
Or just by trying [factordb](https://www.factordb.com).
Then we can find out what `d` is.
First we need to get the coprime numbers of `p` and `q` with the following snippet:
```python
coprimes = (p - 1) * (q - 1)
print("𝜙(𝑛)=", coprimes)
```
Then we get the private key (`d`) with the inverse modulo of `e` and  `𝜙(𝑛)`:
```python
e = 65537
d = inverse(e, coprimes)
```

Finally, we can decrypt the ciphered text (`p`):
``` python
c = 1232131 
plaintext = pow(c, d, n)
flag = long_to_bytes(plaintext) print(flag.decode())
print("Decrypted Plaintext:", flag)
```

