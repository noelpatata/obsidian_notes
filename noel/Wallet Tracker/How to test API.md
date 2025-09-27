# How to send data
## Generate paired keys
``` bash
python -m testing.generate 
```
## Login
Not writing how to login wtf.
## Share key
Make sure to get the public key of the user you created and paste it in the file `testing/public_key.pem` before running this script
``` bash
py -m testing.share "eyy..."
```

## Cipher json object
**Notice:** This script loads the public key by reading a file, make sure that the file it is reading contains the user's server's public key.
Also make sure that the json you are encrypting has double quotes for declaraing the keys and the values, currently the script replaces single quotes with double quotes.
``` bash
py -m testing.cipher "{'name':'Comida'}"
```
## Sign os.env\["SECRET"\]
``` bash
py -m testing.sign
```
## Send request
Won't tell you how to use Postman/Curl
# How to receive data