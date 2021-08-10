from uuid import uuid4
from Crypto.Cipher.PKCS1_OAEP import HashLike
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import hashlib
import rsa


KEY_SIZE = 2048


def gen_key_pair():
    random_generator = Random.new().read
    key = RSA.generate(KEY_SIZE, random_generator)
    private, public = key, key.publickey()
    return public, private


def sign(message, private_key):
    return b64encode(rsa.sign(message, private_key, "SHA-256"))


def verify(message, signature, public_key):
    return rsa.verify(message, b64decode(signature), public_key)


def hash(message):
    return b64encode(hashlib.sha256(message.encode("utf-8")).hexdigest())

def gen_id():
    return str(uuid4())
