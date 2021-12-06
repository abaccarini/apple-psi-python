import cryptography
from h_prime_hkdf import *
from hash_func import *
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
        
        self.alpha = random.randint(1,dh_prime - 1)
        self.L = pow(self.G,self.alpha,self.dh_prime)
        
        
        self.SHARES = []
        self.IDLIST = []

        for i, x_i,in enumerate(X):
            self.ht.add(x_i, i)
        self.pdata = self.generate_pdata()

    def generate_pdata(self):
        p_array = []
        for i in self.ht.array:
            if i is not None:
                p_array.append(pow(H_to_group(i[0][0]), self.alpha, self.dh_prime))
            else:
                p_array.append(random.randint(1,self.dh_prime - 1))
        return p_array
    
    def process_voucher(self, voucher, client_aad):
        
        self.IDLIST.append(voucher.id)
        S_hat = pow(voucher.Q, self.alpha, self.dh_prime)
        H_prime_of_S_hat = H_prime(S_hat)
        
        # rkey_dec = decrypt(H_prime_of_S_hat, voucher.ct, self.nonce)
        
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
            print("both decryptions are successful, adding triple to SHARES")
            self.SHARES.append((voucher.id, dec_adct_sh[0] ,  (dec_adct_sh[1] , dec_adct_sh[2] ) ) )
        else:
            print("one decryption failed, discarding voucher")
        
        
        # set of unique shamir shares
        # we could theoretically just check the x coordinate because we know it will always produce the same y coordinate
        # print("self.SHARES")
        # print(self.SHARES)
        # print(self.SHARES[0])
        # print(self.SHARES[])
        # print()
        t_prime = len(set( [(item[2]) for item in self.SHARES]  ))
        # print("t_prime")
        # print(t_prime)
        
        if t_prime < self.t:
            OUTSET = [item[0] for item in self.SHARES]
            
            return self.IDLIST, OUTSET
        
        # we have exceeded the threshold
        else:
            # distinct_shares = set( [(item[2]) for item in self.SHARES]) 
            # distinct_shares = [(int(item[0].decode('utf-8')), int(item[1].decode('utf-8')) )  for item in distinct_shares]
            
            distinct_shares = [(int(item[0].decode('utf-8')), int(item[1].decode('utf-8')) )  for item in set( [(item[2]) for item in self.SHARES])]
            
            # distinct_shares = [[int((j)) for j in i] for i in distinct_shares]
                        
            # print("distinct_shares")
            # print(distinct_shares)
            
            
            # adkey = reconstruct_secret(distinct_shares)
            adkey = recover_secret(distinct_shares, self.t)
            # print("adkey")
            # print(adkey)
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