import os

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes


BUFFER_SIZE = 1024 * 1024


class AesCipher:
    aes_encrypted_path: str = 'C:/Krypter/Files/encrypted files/AES'
    aes_decrypted_path: str = 'C:/Krypter/Files/decrypted files/AES'

    def __init__(self, in_filename, password):

        self.in_filename = in_filename
        self.out_filename = self.in_filename + '.encrypted'

        self.file_in = open(self.in_filename, 'rb')
        self.password = password

    def encrypt_file(self):

        encrypted_file_path = os.path.join(self.aes_encrypted_path, os.path.basename(self.out_filename))
        file_out = open(encrypted_file_path, 'wb')

        salt = get_random_bytes(32)
        key = scrypt(self.password, salt, key_len=32, N=2 ** 20, r=8, p=1)
        file_out.write(salt)
        cipher = AES.new(key, AES.MODE_GCM)
        file_out.write(cipher.nonce)

        plain_text = self.file_in.read(BUFFER_SIZE)

        while len(plain_text) != 0:
            cipher_text = cipher.encrypt(plain_text)
            file_out.write(cipher_text)
            plain_text = self.file_in.read(BUFFER_SIZE)

        tag = cipher.digest()
        file_out.write(tag)
        file_out.close()

    def decrypt_file(self):
        decryption_status = False
        decrypted_file_path = os.path.join(self.aes_decrypted_path,
                                           os.path.basename(self.file_in.name).removesuffix('.encrypted'))

        size_of_file_in = os.path.getsize(self.file_in.name)
        print(size_of_file_in)
        file_out = open(decrypted_file_path, 'wb')

        block_size = AES.block_size
        salt = self.file_in.read(32)
        print(salt)
        key = scrypt(self.password, salt, key_len=32, N=2 ** 20, r=8, p=1)
        nonce = self.file_in.read(block_size)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        size_of_cipher_text = size_of_file_in - 32 - 16 - 16

        for _ in range(int(size_of_cipher_text / BUFFER_SIZE)):
            data = self.file_in.read(BUFFER_SIZE)
            plain_text = cipher.decrypt(data)
            file_out.write(plain_text)
        data = self.file_in.read(int(size_of_cipher_text % BUFFER_SIZE))
        plain_text = cipher.decrypt(data)
        file_out.write(plain_text)

        tag = self.file_in.read(16)
        try:
            cipher.verify(tag)
            decryption_status = True
        except ValueError:
            self.file_in.close()
            file_out.close()
            os.remove(decrypted_file_path)
        return decryption_status

