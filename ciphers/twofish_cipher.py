import os
from twofish import Twofish


class TwofishCipher:
    tf_encrypted_path: str = 'C:/Krypter/Files/encrypted files/Two fish'
    tf_decrypted_path: str = 'C:/Krypter/Files/decrypted files/Two fish'

    def __init__(self, in_filename, password):

        self.in_filename = in_filename
        self.out_filename = self.in_filename + '.encrypted'
        self.password = password

    def encrypt_file(self):

        encrypted_file_path = os.path.join(
            self.tf_encrypted_path, os.path.basename(self.out_filename))

        file_in = open(self.in_filename, 'r')

        plain_text = file_in.read()

        file_out = open(encrypted_file_path, 'wb')

        block_size = 16

        if len(plain_text) % block_size:
            padded_plain_text = str(
                plain_text + '%' * (block_size - len(plain_text) % block_size)).encode('utf-8')
        else:
            padded_plain_text = plain_text.encode('utf-8')

        twofish = Twofish(str.encode(self.password))
        cipher_text = b''

        for x in range(int(len(padded_plain_text) / block_size)):
            cipher_text += twofish.encrypt(
                padded_plain_text[x * block_size:(x + 1) * block_size])

        file_out.write(cipher_text)

    def decrypt_file(self):

        file_in = open(self.in_filename, 'rb')
        decrypted_file_path = os.path.join(self.tf_decrypted_path, os.path.basename(
            file_in.name).removesuffix('.encrypted'))
        cipher_text = file_in.read()

        file_out = open(decrypted_file_path, 'wb')

        block_size = 16

        twofish = Twofish(str.encode(self.password))
        plain_text = b''

        for x in range(int(len(cipher_text) / block_size)):
            plain_text += twofish.decrypt(
                cipher_text[x * block_size: (x + 1) * block_size])

        file_out.write(str.encode(plain_text.decode('utf-8').strip('%')))
