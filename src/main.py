import numpy as np
import os, random, string
import sys 
import argparse
from nnhash import *
from server import Server
from client import Client
from diffiehellman import DiffieHellman
from structs import *
image_dir = 'images/'
input_dir = 'inputs/'


test_images = os.listdir(image_dir)
X = generate_hash_list(test_images, image_dir)

def main(dh_num, threshold):

    dh1 = DiffieHellman(group=dh_num)
    p = dh1._prime #from group 1
    G = 2
    sh_prime = 2 ** 127 - 1 #12th mersenne prime, may need to make it bigger
    n_prime = 16
    t = threshold

    server = Server(G, p, sh_prime, X, n_prime, t)
    # server.generate_pdata()
    # print(server.ht.array)
    # print(server.pdata)

    # test_inputs = os.listdir(input_dir)
    # Y = generate_hash_list(test_inputs, input_dir)

    # print(Y)

    client = Client(G, p, server.L, server.pdata, t, sh_prime, server.nonce, input_dir)

    print("client.sh_coeff")
    print(client.sh_coeff)


    print("client.adkey_16")
    print(client.adkey_16)

    print("client.triples")
    print(client.triples)
    print()
    # input_triples = client.triple_generation(Y)
    # print(input_triples)


    test_voucher = client.generateVoucher(client.triples[0])
    # print("test_voucher0")
    # print(test_voucher)
    # print()

    server.process_voucher(test_voucher, client.client_aad)

    test_voucher = client.generateVoucher(client.triples[1])
    server.process_voucher(test_voucher, client.client_aad)

    test_voucher = client.generateVoucher(client.triples[2])
    server.process_voucher(test_voucher, client.client_aad)

    test_voucher = client.generateVoucher(client.triples[3])
    print(server.process_voucher(test_voucher, client.client_aad))
    
    return 0



if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser(description = 'Apple PSI proof of concept',formatter_class=argparse.ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
    parser.add_argument('--dh_num', type=int, default=1, help='Diffie-Hellman group number', metavar = 'DH_GROUP_ID')
    parser.add_argument('--thresh', type=int, default=2, help='Shamir SS threshold t', metavar = 'THRESHOLD')
    
    
    args = parser.parse_args()
    # print(args)
    options = vars(args)
    print('Provided arguments: ' + str(options))
    # print(args.dh_num)
    # print(args.thresh)
    sys.exit(main(args.dh_num, args.thresh)) 
