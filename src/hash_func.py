# file is used for constructing H:{0,1}* -> G prime p
import numpy as np
import os
import hashlib
import hmac
from nnhash import *
from diffiehellman import DiffieHellman
import random


dh1 = DiffieHellman(group=1, key_bits=540)


#takes a hash x
def H_to_group(x):

    p = dh1._prime #from group 1
    # print(p)
    # test_images = os.listdir('images/')

    # x = generate_hash_list(test_images)
    # print(x)
    # test_index = 2
    # test_hash = x[test_index] #will also represent a client's input

    key = 0x11
    # x = test_hash

    h = hmac.new(str(key).encode(), str(x).encode(), hashlib.sha256).hexdigest()
    # print("h:")
    # print(h)


    # print("int(h):")
    # print(int(h, 16))

    # print("int(h) mod p:")
    # print(int(h, 16) % p)

    # print("int(h)^2 mod p:")
    # print(pow(int(h, 16),2,p))



    # print("((int(h) mod (p -1)) + 1)^2 mod p:")
    # # print(pow((int(h, 16) % (p - 1) + 1) ,2,p))
    # print()
    # H_out = pow((int(h, 16) % (p - 1) + 1) ,1,p)
    H_out = int(h, 16) % (p)
    
    return H_out


def ht_hash(input, n_prime):
    # print(key)
    """Get the index of our array for a specific string key"""
    
    h = hashlib.sha256((input).encode('utf-8'))
    return int(h.hexdigest(), 16) % n_prime


# alpha = random.randint(1,p - 1)

# print(alpha)

# print(pow(H_out, alpha, p) )