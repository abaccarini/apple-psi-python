import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
data = b"a secret message"
# aad = b"authenticated but unencrypted data"
aad = None
key = AESGCM.generate_key(bit_length=128)
key2 = AESGCM.generate_key(bit_length=128)
aesgcm = AESGCM(key)
nonce = os.urandom(13)
ct = aesgcm.encrypt(nonce, data, aad)
aesgcm2 = AESGCM(key2)

print(aesgcm2.decrypt(nonce, ct, None))
# print(aesgcm.decrypt(nonce, ct, aad))
