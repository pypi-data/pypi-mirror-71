import hashlib
from bitarray import bitarray

def get_sha256_hash_arr(hashId, dataString):
    message = hashlib.sha256()

    message.update((str(hashId) + dataString).encode("utf8"))

    message_in_bytes = message.digest()

    message_in_bit_array = bitarray(endian='little')
    message_in_bit_array.frombytes(message_in_bytes)

    return message_in_bit_array