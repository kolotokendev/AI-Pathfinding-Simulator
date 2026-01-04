import hashlib

# Tvoj fake header (64 bajta = 512 bit)
header = bytes.fromhex(
    "0100000000000000000000000000000000000000000000000000000000000000"
    "5f5b5b5b"   # timer (32-bit)
    "1d00ffff"   # bits (32-bit)
    "0000000b"   # nonce = 11
    + "00"*44    # padding da bude 64B
)

# SHA256d
hash1 = hashlib.sha256(header).digest()
hash2 = hashlib.sha256(hash1).hexdigest()
print(hash2)
