import random
import string

# Functions to encrypt and decrypt the string

def generate_key():
	key = ''.join(random.choices(string.digits, k=5))
	return key


def encrypt(string, key):
	enc_str = ""
	counter = 1
	key_index = 0

	for i in string:
		if counter % 2 == 0:
			enc_str += chr(ord(i) - (int(key[key_index]) * 2))
		else:
			enc_str += chr(ord(i) + (int(key[key_index]) * 3))

		counter += 1
		key_index += 1
		if key_index >= 5:
			key_index = 0

	return enc_str


def decrypt(string, key):
	dec_str = ""
	counter = 1
	key_index = 0

	for i in string:
		if counter % 2 == 0:
			dec_str += chr(ord(i) + (int(key[key_index]) * 2))
		else:
			dec_str += chr(ord(i) - (int(key[key_index]) * 3))

		counter += 1
		key_index += 1
		if key_index >= 5:
			key_index = 0

	return dec_str

"""
test = "Helo World"
key = generate_key()
print(key)
enc = encrypt(test, key)
print(enc)
dec = decrypt(enc, key)
print(dec)

print(len(enc))
print(len(dec))
"""
