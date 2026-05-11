import hashlib

# (B303: blacklist MD5)
def insecure_hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()