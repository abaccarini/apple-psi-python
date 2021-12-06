import os, random
# from cryptography import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import hmac
import hashlib

# from shamir import *
# Salts should be randomly generated

def encrypt(key, message, nonce, aad):
    if type(message) is str:
        b_message = bytes(message,'utf-8')
    elif type(message) is bytes:
        b_message = message
    else:
        print( "ERROR: message is neither string or bytes")
        return -1
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, b_message, aad)
    return ct

def decrypt(key, ctext, nonce, aad):
    aesgcm = AESGCM(key)
    ptext = aesgcm.decrypt(nonce, ctext, aad)
    return ptext


def generate_fkey():
    salt = os.urandom(16)
    # salt = b'\x16\xd7\xb6\x98\xee\xd1\xc2\xcd\x1b\xeaT\xbeK\xdb:\x13'
    hkdf = HKDF( algorithm=hashes.SHA256(), length=32, salt=salt, info=None)
    key = hkdf.derive(b"input key")
    return key

def generate_adkey(dh_prime):
    # return H_prime(random.randint(1,2**127 - 1)) #change to actual random value
    ran = random.randint(1,2**32 - 1)
    # print("ran")
    # print(ran)
    # ran = 2358485516
    return H_prime(ran) #change to actual random value
    # return H_prime(4) #change to actual random value

def generate_rkey(dh_prime):
    return H_prime(random.randint(1,dh_prime - 1)) #change to actual random value
    # return H_prime(5) #change to actual random value

def H_prime(group_ele):
    salt = b'Ue\xad\x93/\x87\xc6\xcd\x81;\xc0\xef\xad7~\xde'
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        info=None,
    )
    # key = hkdf.derive(bytes(str(group_ele),encoding='utf-8'))
    key = hkdf.derive(str(group_ele).encode())
    return key


# sh_prime is the shamir field prime
def prf_F(fkey, id, sh_prime):
    h = hmac.new(str(fkey).encode(), str(id).encode(), hashlib.sha256).hexdigest()
    return (int(h,16) % sh_prime)
    
#returns a random field element
def generate_field_element(p):
    return random.randint(1,p - 1)

def generate_beta_gamma(p):
    return random.randint(1,p - 1), random.randint(1,p - 1)

def compute_Q_S(G, P_w, L, p, Hy):
    beta, gamma  = generate_beta_gamma(p)
    # beta = 336987840739067645353750384631303108611880609887326415281167359896349535214638476893090672442788683495430136298637403913036022658315097543277828917323443666970026163458371568336662208869449372019082118604077653351476117412097770508 
    # gamma = 786391032311386506087782616250068037865467535014149629712627858528666303117677195672572493371376685674198851339345922613958014565578685512420750583095698449944144701649236118574318394800014495715782898274021876401369307155346355033
    Q = (pow(Hy, beta, p) * pow(G, gamma, p)) % p
    S = (pow(P_w, beta, p) * pow(L, gamma, p)) % p
    return Q,S

# Hash functions ######
# big H, produces a group element in G mod p 
def H_to_group(x, p):
    key = 0x11
    h = hmac.new(str(key).encode(), (x).encode(), hashlib.sha256).hexdigest()
    H_out = int(h, 16) % (p)
    # H_out = pow((int(h, 16) % (p - 1) + 1) ,1,p)

    return H_out

# little h
def ht_hash(input, n_prime):
    h = hashlib.sha256((input).encode('utf-8'))
    return int(h.hexdigest(), 16) % n_prime

