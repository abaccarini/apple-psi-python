from crypto_ops import *
from nnhash import generate_hash_list
from shamir import *
from structs import *
import string

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Client:
    def __init__(self, G, dh_prime, L, pdata, t, sh_prime, nonce, input_dir):
        self.L = L
        self.G = G
        self.dh_prime = dh_prime
        self.pdata = pdata
        self.nonce = nonce
        self.n_prime = len(pdata)
        self.sh_prime = sh_prime
        self.adkey = generate_adkey(self.dh_prime)
        self.fkey = generate_fkey()
        self.adkey_16 = int.from_bytes(self.adkey, byteorder='big')
        self.sh_coeff = coeff(t, self.adkey_16, sh_prime)
        
        #generating random bytestring for client
        self.client_aad = os.urandom(4)
        test_inputs = os.listdir(input_dir)
        self.Y = generate_hash_list(test_inputs, input_dir) 
        self.triples = self.triple_generation()
    
    def triple_generation(self):
        id_seq = 0
        ad_seq = 0
        triples = []
        for y in self.Y:
            t_id = 'id_' + '%03d' % id_seq + '_'+ id_generator(size = 9)
            t_ad = 'ad_' + '%05d' % ad_seq
            id_seq +=1
            ad_seq +=1

            triples.append(Triple(y, t_id, t_ad))
            
        return triples
    

    
    
    def generateVoucher(self, trip):
        adct = encrypt(self.adkey, trip.ad, self.nonce, self.client_aad)
        x = prf_F(self.fkey, trip.id, self.sh_prime)
        fox = polynom(x, self.sh_coeff)
        rkey = generate_rkey(self.dh_prime)
        # x and fox are ints, adct is bytes, need to convert 
        rct = (encrypt(rkey, adct, self.nonce, self.client_aad),
               encrypt(rkey, str(x), self.nonce, self.client_aad), 
               encrypt(rkey, str(fox), self.nonce, self.client_aad))
    
        w = ht_hash(trip.y, self.n_prime)
        P_w = self.pdata[w]
        H_y = H_to_group(trip.y, self.dh_prime)
        Q, S = compute_Q_S(self.G, P_w, self.L, self.dh_prime, H_y)
        Hp_o_S = H_prime(S)
        ct = encrypt(Hp_o_S, rkey, self.nonce, self.client_aad)

        voucher = Voucher(trip.id, Q, ct, rct)
        return voucher
# test_triple = triple("id_123465789", "id_123465789","some_associated_data_of_y")
# print(test_triple.y)