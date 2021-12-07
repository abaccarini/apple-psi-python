import os
import math
import sys 
import argparse
from nnhash import *
from server import Server
from client import Client
# import diffiehellman
from diffiehellman.diffiehellman import DiffieHellman
from structs import *
image_dir = 'images/'
input_dir = 'inputs/'


def main(dh_num, threshold):
    print("------------------------")

    test_images = os.listdir(image_dir)
    X = generate_hash_list(test_images, image_dir)
    dh1 = DiffieHellman(group=dh_num)
    p = dh1.prime #from group 1
    G = 2
    sh_prime = 2 ** 521 - 1 #13th mersenne prime, may need to make it bigger
    n_prime = 2 ** math.ceil(math.log(len(test_images),2)+1)
    t = threshold

    print("Initalizing server...")
    server = Server(G, p, sh_prime, X, n_prime, t)
    
    print("Initalizing client...")
    client = Client(G, p, server.L, server.pdata, t, sh_prime, server.nonce, input_dir)


    print("---\nExperiment 1: client submits y in X")

    test_voucher = client.generateVoucher(client.triples[0])
    IDLIST, OUTSET = server.process_voucher(test_voucher, client.client_aad)
    print("IDLIST ", IDLIST, "\nOUTSET ", OUTSET)


    print("---\nExperiment 2: client submits y in X again")

    test_voucher = client.generateVoucher(client.triples[0])
    IDLIST, OUTSET = server.process_voucher(test_voucher, client.client_aad)
    print("IDLIST ", IDLIST, "\nOUTSET ", OUTSET)

    print("\n---\nExperiment 3: client submits y in X, but with a different id")
    test_voucher = client.generateVoucher(client.triples[1])
    IDLIST, OUTSET = server.process_voucher(test_voucher, client.client_aad)
    print("IDLIST ", IDLIST, "\nOUTSET ", OUTSET)

    print("\n---\nExperiment 4: client submits y not in X")
    test_voucher = client.generateVoucher(client.triples[2])
    IDLIST, OUTSET = server.process_voucher(test_voucher, client.client_aad)
    print("IDLIST ", IDLIST, "\nOUTSET ", OUTSET)

    print("\n---\nExperiment 5: client submits different y in X")
    test_voucher = client.generateVoucher(client.triples[3])
    IDLIST, OUTSET = server.process_voucher(test_voucher, client.client_aad)
    print("IDLIST ", IDLIST, "\nOUTSET ", OUTSET)
    print("\n------------------------")
    return 0


def single_image(dh_num, threshold, input_image):

    test_images = os.listdir(image_dir)
    X = generate_hash_list(test_images, image_dir)
    dh1 = DiffieHellman(group=dh_num)
    p = dh1._prime #from group 1
    G = 2
    sh_prime = 2 ** 521 - 1 #13th mersenne prime, may need to make it bigger
    n_prime = 6
    t = threshold

    print("Initalizing server...")
    server = Server(G, p, sh_prime, X, n_prime, t)
    
    print(server.ht.array)
    
    print("Initalizing client...")
    client = Client(G, p, server.L, server.pdata, t, sh_prime, server.nonce, input_dir, input_image)

    test_voucher = client.generateVoucher(client.triples[0])
    IDLIST, OUTSET = server.process_voucher(test_voucher, client.client_aad)
    print("IDLIST ", IDLIST, "\nOUTSET ", OUTSET)

    return 0



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description = 'Apple PSI proof of concept',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, 
        conflict_handler='resolve')

    class ThresholdAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if values < 2:
                parser.error("Minimum threshold for {0} is 2".format(option_string))
            setattr(namespace, self.dest, values)

    parser.add_argument('-d', 
                        '--dh_num', 
                        type=int, 
                        default=14, 
                        choices=[1, 2, 5, 14, 15, 16], 
                        help='Diffie-Hellman group number = [1, 2, 5, 14, 15, 16]', 
                        metavar = '\b'
                        )
    
    parser.add_argument('-t',
                        '--thresh', 
                        action=ThresholdAction,
                        type=int, 
                        default=3, 
                        help='Shamir SS threshold t >= 2', metavar = '\b')
    
    parser.add_argument('-i',
                        '--image', 
                        type=str, 
                        nargs=1,
                        default=None,
                        help='Input image, must be in inputs/ directory', 
                        metavar = '\b'
                        )
    
    args = parser.parse_args()
    
    if args.image is None:
        sys.exit(main(args.dh_num, args.thresh)) 
    else:
        sys.exit(single_image(args.dh_num, args.thresh, args.image)) 
        