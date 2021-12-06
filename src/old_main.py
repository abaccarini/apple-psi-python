import numpy as np
import os
import hashlib
import hmac
import random
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# import onnx
# import cryptography
from nnhash import *
from structs import *
from hash_table import *
from crypto_ops import *
from Crypto.Util import number

from diffiehellman import DiffieHellman
image_dir = 'images/'
input_dir = 'inputs/'


dh1 = DiffieHellman(group=1, key_bits=540)
p = dh1._prime #from group 1
G = 2
# automatically generate two key pairs

test_images = os.listdir('images/')
print(test_images)

x = generate_hash_list(test_images, image_dir)
print(x)

y = x[0]
print("sample client image hash:")
print(y)

# must be greater than or equal to 16 for 3 inputs


n_prime = 16
ht = HashTable(n_prime) 

# hash_nonce = 63

for i, x_i,in enumerate(x):
    # print(x_i)
    ht.add(x_i, i)


test_index = 2
test_hash = x[test_index] #will also represent a client's input
print("test_hash")
print(test_hash)
# h = hashlib.sha256(test_hash.encode('utf-8'))
# print(h)

# print(int(h.hexdigest(), 16))
# print()
# print()
# print()
# print(ht.array)
# print()
# print("ind: " + str(test_index) + ", x_i : " + x[test_index] +"\n")

# print(ht.array[19])
# print(ht.array[20])
for i in ht.array:
    if i is not None:
        print(i)
print()

print(ht.get(test_hash)) # we don't care about the value
print(ht.hash(test_hash)) 
# should return the index in the table where test_hash is stored, this is the "hash" function that gets sent to the client
# the index that is returned is w, and that is what the client uses to retrieve P_w


def generate_pdata(ht, alpha):
    p_array = []
    for i in ht.array:
        if i is not None:
            p_array.append(pow(H_to_group(i[0][0]), alpha, p))
            # print(i[0][0])
        else:
            p_array.append(random.randint(1,p - 1))
    return p_array
            

# alpha = random.randint(1,p - 1)
alpha = 478205330694918742080786118987921092155630507787471757349489612947297928351578612853826307541572847242261016987971261091746891593288837317851442674228234581601389984369825747588381558381331423481031759388856471038616263000722496377
print("alpha")
print(alpha)

pdata = generate_pdata(ht, alpha)
print(pdata)
print("len(pdata)")
print(len(pdata))

L = pow(G,alpha,p)
print("L")
print(L)


id = "id_123465789"
ad = "some_associated_data_of_y"



test_triple = Triple(test_hash, id, ad)

print(test_triple)

adkey = generate_adkey()
fkey = generate_fkey()
rkey = generate_rkey()

print("adkey :  " + str(adkey))
adkey_16 = int.from_bytes(adkey, byteorder='big')

print("len(adkey) :  " + str(len(adkey)))

print("adkey 16:  " + str(adkey_16))


print("adkey bitlen : " + str (adkey_16.bit_length()))
print("fkey  :  " + str(fkey))
print("rkey  :  " + str(rkey))


# adct = encrypt(adkey, test_triple.ad, client_aad)

# nonce = os.urandom(12) #96 bit nonce (12 * 8 = 96)
# fixing the nonce for testing
nonce = b'\x88\xbd!\xdb*\x98\x95\xf6\x92\x07\xbd\x80'
client_aad = b"client_authentication"

adct = encrypt(adkey, test_triple.ad, nonce, client_aad)

print("adct : ")
print(adct)

# this output space needs to be the size of the shamir field
# shrink accoridngly
#need a 128-bit shamir prime

# sh_prime = number.getPrime(128)
# sh_prime = 298903382765612224736228570049312759983
sh_prime = 2 ** 127 - 1 #12th mersenne prime, may need to make it bigger

t = 3
print("sh_prime")
print(sh_prime)
x = prf_F(fkey, test_triple.id, sh_prime)
print("x : ")
print(x)
# sh_coeff = coeff(t, int.from_bytes(adkey, byteorder='big'), sh_prime)
sh_coeff = [7263977247803331747363854460124156686, 95679112334543203228676394260209128331, adkey_16]
print(sh_coeff)

fox = polynom(x, sh_coeff)
print("fox")
print(fox)

# sh = (x.to_bytes(16,'big'))
# sh = (fox.to_bytes(16,'big'))
sh = str(x)
# sh = ';'+str(x) + ',' + str(fox)
# sh = bytes(sh,'utf-8')
print("sh")
print(sh)

print("x.to_bytes()")
print(x.to_bytes(16,'big'))

# adct_sh = adct+sh
adct_sh = sh
print(adct_sh)

rct = encrypt(rkey, adct_sh, nonce, client_aad)


w = ht_hash(test_triple.y, n_prime)
print(w)

# print(int(x, 16))
P_w = pdata[w]
print(P_w)

H_y = H_to_group(test_triple.y)


Q, S = compute_Q_S(G, P_w, L, p, H_y)


print("Q")
print(Q)
print("S")
print(S)
H_prime_of_S = H_prime(S)

print("H_prime_of_S")
print(H_prime_of_S)

ct = encrypt(H_prime_of_S, rkey, nonce, client_aad)
print("ct")
print(ct)


S_hat = pow(Q, alpha, p)
print("S_hat")
print(S_hat)

H_prime_of_S_hat = H_prime(S_hat)


print("H_prime_of_S_hat")
print(H_prime_of_S_hat)

# while True:
try:
    rkey_dec = decrypt(H_prime_of_S_hat, ct, nonce, client_aad)
    print("DECRYPTION 1 SUCCESSFUL")
    dec_adct_sh = decrypt(rkey_dec, rct, nonce, client_aad)
    print("DECRYPTION 2 SUCCESSFUL")
    
    # break
except cryptography.exceptions.InvalidTag:
    print("DECRYPTION FAILED")
    # break


# rkey_dec = decrypt(H_prime_of_S_hat, ct, nonce, client_aad)
print("rkey_dec")
print(rkey_dec)


print("dec_adct_sh")
print(dec_adct_sh)



print("dec_adct_sh.from_bytes(")
# print(int.from_bytes(dec_adct_sh, byteorder='big'))
print(dec_adct_sh.decode('utf-8'))
