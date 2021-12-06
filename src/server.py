import cryptography
from crypto_ops import *
from shamir import *
from structs import *
from hash_table import *

class Server:
    def __init__(self, G, dh_prime, sh_prime, X, n_prime, t):
        self.nonce = os.urandom(12) #96 bit nonce (12 * 8 = 96)
        self.G = G
        self.dh_prime = dh_prime
        self.sh_prime = sh_prime
        self.n_prime = n_prime
        self.t = t
        self.ht = HashTable(self.n_prime)
        self.t_prime = 0
        self.alpha = random.randint(1,dh_prime - 1)
        self.L = pow(self.G,self.alpha,self.dh_prime)
        
        self.SHARES = []
        self.IDLIST = []

        for i, x_i,in enumerate(X):
            self.ht.add(x_i, i)
        # ensuring every bucket has at most one item
        for item in self.ht.array:
            if item is  None or len(item) == 1:
                pass
            else:
                print('bucket BAD -- INCRREASE TABLE SIZE')
        self.pdata = self.generate_pdata()

    def generate_pdata(self):
        p_array = []
        for i in self.ht.array:
            if i is not None:
                p_array.append(pow(H_to_group(i[0][0], self.dh_prime), self.alpha, self.dh_prime))
            else:
                p_array.append(random.randint(1,self.dh_prime - 1))
        return p_array
    
    def process_voucher(self, voucher, client_aad):
        
        self.IDLIST.append(voucher.id)
        S_hat = pow(voucher.Q, self.alpha, self.dh_prime)
        H_prime_of_S_hat = H_prime(S_hat)
        goodkey = False
        try:
            rkey_dec = decrypt(H_prime_of_S_hat, voucher.ct, self.nonce, client_aad)
            dec_adct_sh = ()
            for rct in voucher.rct:
                dec_adct_sh += (decrypt(rkey_dec, rct, self.nonce, client_aad),)
            goodkey = True
        except cryptography.exceptions.InvalidTag:
            pass
        if goodkey:
            print("\tboth decryptions are successful, adding triple to SHARES")
            self.SHARES.append((voucher.id, dec_adct_sh[0] ,  (dec_adct_sh[1] , dec_adct_sh[2] ) ) )
            self.t_prime = len(set( [(item[2]) for item in self.SHARES]  ))
        else:
            print("\tone decryption failed, discarding voucher")
        
        
        # print("t_prime = "+str(self.t_prime)) 
        if self.t_prime < self.t:
            print("\tThreshold not met")
            OUTSET = [item[0] for item in self.SHARES]
            return self.IDLIST, OUTSET
        else:
            print("\tThreshold exceeded, reconstructing adkey")
            distinct_shares = [(int(item[0].decode('utf-8')), int(item[1].decode('utf-8')) )  for item in set( [(item[2]) for item in self.SHARES])]
            adkey = recover_secret(distinct_shares, self.t)
            # print("adkey")
            # print(adkey)
            # converting to bytes 
            adkey_bytes = adkey.to_bytes(16, 'big')
            id_adcts = [(item[0], item[1]) for item in self.SHARES]
            OUTSET = []
            for id_adct in id_adcts:
                try:
                    ad = decrypt(adkey_bytes, id_adct[1], self.nonce, client_aad)
                    OUTSET.append((id_adct[0], ad))
                except cryptography.exceptions.InvalidTag:
                    # corresponding voucher is invalid, need to remove id from IDLIST
                    print('voucher invalid') 
                    pass

            return self.IDLIST, OUTSET