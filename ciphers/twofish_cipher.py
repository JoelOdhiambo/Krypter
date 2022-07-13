import os
from twofish import Twofish

class TwofishCipher:
    
    def __init__(self,in_filename, password):
        
        self.in_filename=in_filename
        self.out_filename=self.in_filename+'.encrypted'
        
        self.file_in=open(self.in_filename,'rb')
        self.password=password
    
    def encrypt_file(self):
        # try:
        #     with open('infile.txt','r') as file_in:
        #         plain_text=file_in.read()   
        # except  FileNotFoundError:
        #     print("File does not exist!")
        
        save_path='C:\Krypter\Files\encrypted files\Two fish'
        file_path=os.path.join(save_path,os.path.basename(self.out_filename))
        plain_text=self.file_in.read()
      
        file_out= open(file_path,'wb')
        
        block_size=16
        
        if len(plain_text) % block_size:
            padded_plain_text=str(plain_text+ '%' * (block_size-len(plain_text)%block_size)).encode('utf-8')
        else:
            padded_plain_text=plain_text.encode('utf-8')
        
        twofish=Twofish(str.encode(self.password))
        cipher_text=b''
        
        for x in range(int(len(padded_plain_text)/ block_size)):
            cipher_text += twofish.encrypt(padded_plain_text[x * block_size:(x + 1) * block_size])
            
        file_out.write(cipher_text)
        
    
    def decrypt_file(self,file_in,file_out, password):
        try:
            with open('infile.encrypted.txt','rb') as file_in:
                cipher_text=file_in.read() 
        except  FileNotFoundError:
            print("File does not exist!")
      
        file_out= open(file_out,'wb')
        
        block_size=16
        
        twofish=Twofish(str.encode(password))
        plain_text=b''
        
        for x in range(int(len(cipher_text)/block_size)):
            plain_text += twofish.decrypt(cipher_text[x * block_size: (x+1) * block_size])
            
        file_out.write(str.encode(plain_text.decode('utf-8').strip('%')))
    
if __name__ == '__main__':
    twofish=TwofishCipher()
    
    password='12345'
    
    file_in='infile.txt'
    file_out='infile.encrypted.txt'
    twofish.encrypt_file(file_in, file_out, password) 
    
    file_in='infile.encrypted.txt'
    file_out='infile.decrypted.txt'
    twofish.decrypt_file(file_in, file_out, password)    
 
    