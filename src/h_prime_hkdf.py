import os
# from cryptography import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import hmac
import hashlib

from shamir import *
# Salts should be randomly generated

# salt = os.urandom(16)
# print(salt)

def H_prime(group_ele):
    
    salt = b'Ue\xad\x93/\x87\xc6\xcd\x81;\xc0\xef\xad7~\xde'
    # info = b"hkdf-example"
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        info=None,
    )
    key = hkdf.derive(bytes(str(group_ele),encoding='utf-8'))
    return key

# print(H_prime(4))


def encrypt(key, message, nonce, aad):
    
    
    # nonce = os.urandom(12) #96 bit nonce (12 * 8 = 96)
    if type(message) is str:
        b_message = bytes(message,'utf-8')
    # if type(message) is int:
        # b_message = message.to_bytes(16,'big')
    elif type(message) is bytes:
        b_message = message
    else:
        print( "ERROR: message is neither string or bytes")
        return -1
    # print("b_message")
    # print(b_message)
    aesgcm = AESGCM(key)

    ct = aesgcm.encrypt(nonce, b_message, aad)

    # iv = os.urandom(16)
    # cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    # encryptor = cipher.encryptor()
    # ct = encryptor.update(b_message) + encryptor.finalize()
    # print(ct)
    return ct


def decrypt(key, ctext, nonce, aad):
    aesgcm = AESGCM(key)
    ptext = aesgcm.decrypt(nonce, ctext, aad)
    return ptext

    # decryptor = cipher.decryptor()
    # pt = decryptor.update(ct) + decryptor.finalize()
    # print(pt)



def generate_fkey():
    # salt = os.urandom(16)
    # print("salt")
    # print(salt)
    salt = b'\x16\xd7\xb6\x98\xee\xd1\xc2\xcd\x1b\xeaT\xbeK\xdb:\x13'
    hkdf = HKDF( algorithm=hashes.SHA256(), length=32, salt=salt, info=None)
    key = hkdf.derive(b"input key")
    return key

def generate_adkey():
    return H_prime(4) #change to actual random value


def generate_rkey():
    return H_prime(5) #change to actual random value


# fkey expected to
# sh_prime is the shamir field prime
def prf_F(fkey, id, sh_prime):
    # key = 0x11
    
    h = hmac.new(str(fkey).encode(), str(id).encode(), hashlib.sha256).hexdigest()
    # print("h : ")
    # print(h)
    return (int(h,16) % sh_prime)
    # return (int(h,16))
    
#returns a random field element
def generate_field_element(p):
    return random.randint(1,p - 1)


def generate_beta_gamma(p):
    return random.randint(1,p - 1), random.randint(1,p - 1)

def compute_Q_S(G, P_w, L, p, Hy):
    # beta, gamma  = generate_beta_gamma(p)
    
    beta = 336987840739067645353750384631303108611880609887326415281167359896349535214638476893090672442788683495430136298637403913036022658315097543277828917323443666970026163458371568336662208869449372019082118604077653351476117412097770508 
    gamma = 786391032311386506087782616250068037865467535014149629712627858528666303117677195672572493371376685674198851339345922613958014565578685512420750583095698449944144701649236118574318394800014495715782898274021876401369307155346355033
    
    
    Q = (pow(Hy, beta, p) * pow(G, gamma, p)) % p
    S = (pow(P_w, beta, p) * pow(L, gamma, p)) % p
    
    return Q,S







adkey = H_prime(4)
# print("adkey")
# print(adkey)
# print()
# # we need to do this when we use shamir secret sharing
# print(int.from_bytes(adkey, byteorder='big'))

fkey = generate_fkey()
# print(fkey)


id = "id_123465789"
ad = "some_associated_data"

# x = prf_F(fkey, id)
# print("x : ")
# print(x)
# print(int(x, 16))




# ct = encrypt(adkey, ad)
# print(ct)

