import os
import shutil
from functools import partial
import tkinter as tk
from tkinter import DISABLED, Frame, Label, Menu, PhotoImage, StringVar, ttk
from tkinter import filedialog

import random
import string

import ciphers.twofish_cipher
from ciphers.aes_cipher import AesCipher as aes_cipher
from ciphers.twofish_cipher import TwofishCipher as two_fish

MAX_PASSWORD_LENGTH = 16


class KrypterApp(tk.Tk, ciphers.twofish_cipher.TwofishCipher, ciphers.aes_cipher.AesCipher):
    def __init__(self):
        super().__init__()

        self.app_dir = 'C:/Krypter/Files'

        list = ('original files', 'encrypted files/AES',
                'encrypted files/Twofish')

        app_path = partial(os.path.join, self.app_dir)
        make_directory = partial(os.makedirs, exist_ok=True)

        for directories in map(app_path, list):
            make_directory(directories)

        self.title('Krypter')
        self.tk.call('wm', 'iconphoto', self._w,
                     tk.PhotoImage(file='icons\Krypter Icon.png'))
        self.geometry('500x500')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # self.menu_bar = Menu(self)

        # self.config(menu=self.menu_bar)

        # self.file_menu = Menu(self.menu_bar, tearoff=0)
        # self.file_menu.add_command(
        #     label="Open",
        #     command=self.open_file
        # )

        # self.file_menu.add_separator()

        # self.sub_menu = Menu(self.file_menu, tearoff=0)

        # self.sub_menu.add_command(label='Toggle Dark Mode')
        # self.file_menu.add_cascade(
        #     label="Preferences",
        #     menu=self.sub_menu
        # )

        # self.file_menu.add_separator()

        # self.file_menu.add_command(
        #     label="Quit",
        #     command=self.destroy
        # )

        # self.menu_bar.add_cascade(
        #     label="File",
        #     menu=self.file_menu,
        #     underline=0
        # )

        # self.encrypt_menu = Menu(self.menu_bar, tearoff=0)

        # self.menu_bar.add_cascade(
        #     label="Encrypt",
        #     menu=self.encrypt_menu,
        #     command=self.change_to_encrypt

        # )

        # self.decrypt_menu = Menu(self.menu_bar, tearoff=0)

        # self.menu_bar.add_cascade(
        #     label="Decrypt",
        #     menu=self.decrypt_menu,
        #     command=self.change_to_decrypt
        # )

        self.notebook = ttk.Notebook(self)

        self.encrypt_frame = Frame(self.notebook)

        self.decrypt_frame = Frame(self.notebook)

        self.notebook.pack(expand=1, fill="both")

        self.notebook.add(self.encrypt_frame, text="Encrypt")
        self.notebook.add(self.decrypt_frame, text="Decrypt")

        self.label_choose = Label(self.encrypt_frame, text="1. Choose file to encrypt")
        self.label_choose.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # File to encrypt Path Variable
        self.original_file_path = StringVar(None)

        self.original_file_entry = ttk.Entry(self.encrypt_frame, width=44)
        self.original_file_entry.grid(column=0, row=1, sticky=tk.W, padx=20, pady=5)

        self.bool_one = StringVar(None)
        self.choose_button_one = ttk.Button(self.encrypt_frame,
                                            text="Choose File", name="btn_one", command=self.open_original_file)
        self.choose_button_one.grid(column=1, row=1, sticky=tk.W, pady=5)

        self.label_two = Label(
            self.encrypt_frame, text="2. Enter a password and choose an Encryption Algorithm")
        self.label_two.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.default_password_var = tk.StringVar(None)

        self.password_entry = ttk.Entry(
            self.encrypt_frame, textvariable=self.default_password_var, width=44)
        self.password_entry.grid(column=0, row=3, sticky=tk.W, padx=20, pady=5)

        self.generate_button = ttk.Button(self.encrypt_frame,
                                          text="Generate Password", command=self.password_generator)
        self.generate_button.grid(column=1, row=3, sticky=tk.W, pady=5)

        self.check_button = ttk.Checkbutton(
            self.encrypt_frame, text="Hide Password", onvalue=False, offvalue=True, command=self.toggle_password)

        self.check_button.grid(column=0, row=4, sticky=tk.W, padx=100)

        self.radio_var = StringVar(None)
        self.aes_radio_button_e = ttk.Radiobutton(self.encrypt_frame,
                                                  text='AES',
                                                  variable=self.radio_var,
                                                  value=1)
        self.aes_radio_button_e.grid(column=0, row=5, sticky=tk.W, padx=19)
        self.two_fish_radio_button_e = ttk.Radiobutton(self.encrypt_frame,
                                                       text='Twofish',
                                                       variable=self.radio_var,
                                                       value=2)
        self.two_fish_radio_button_e.grid(column=0, row=6, sticky=tk.W, padx=19)

        self.label_three = Label(
            self.encrypt_frame, text="3. Encryption")
        self.label_three.grid(column=0, row=7, sticky=tk.W, padx=5, pady=10)

        self.encrypted_file_dir_var = StringVar(None)

        self.label_four = Label(
            self.encrypt_frame, text="Working Directory: ")
        self.label_four.grid(column=0, row=8, sticky=tk.W, padx=17, pady=5)

        self.original_file_var = StringVar(None)

        self.encrypted_file_dest = ttk.Entry(
            self.encrypt_frame, width=44)

        self.encrypted_file_dest.config(state=DISABLED)
        self.encrypted_file_dest.place(x=130, y=242)

        self.encryption_photo = PhotoImage(
            file=r"icons\wicons8-password-50.png")
        self.encryption_photo_image = self.encryption_photo.subsample(3, 3)

        self.encrypt_button = ttk.Button(self.encrypt_frame,
                                         text="Encrypt", command=self.selected)
        self.encrypt_button.grid(column=0, row=9, sticky=tk.W, padx=19, pady=5)

        # self.separator_two = ttk.Separator(self, orient='horizontal')
        # self.separator_two.place(relx=0, rely=0.95, relheight=0.5, relwidth=1)

        # self.progress_bar=ttk.Progressbar(self,orient='horizontal',mode='indeterminate',length=100)
        # self.progress_bar.place(x=1,y=453)

        self.label_choose_d = Label(self.decrypt_frame, text="1. Choose file to decrypt")
        self.label_choose_d.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # File to decrypt path variable
        self.encrypted_file_path = StringVar(None)

        self.encrypted_file_entry = ttk.Entry(
            self.decrypt_frame, width=44)
        self.encrypted_file_entry.grid(column=0, row=1, sticky=tk.W, padx=20, pady=5)

        self.bool_two = StringVar(None)
        self.choose_button_two = ttk.Button(self.decrypt_frame,
                                            text="Choose File ", name="btn_two", command=self.open_encrypted_file)
        self.choose_button_two.grid(column=1, row=1, sticky=tk.W, pady=5)

        self.label_two = Label(
            self.decrypt_frame, text="2. Enter your password and choose a Decryption Algorithm")
        self.label_two.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.default_password_var = tk.StringVar(None)

        self.password_entry = ttk.Entry(
            self.decrypt_frame, textvariable=self.default_password_var, width=44)
        self.password_entry.grid(column=0, row=3, sticky=tk.W, padx=20, pady=5)

        self.check_button = ttk.Checkbutton(
            self.decrypt_frame, text="Hide Password", onvalue=False, offvalue=True, command=self.toggle_password)

        self.check_button.grid(column=0, row=4, sticky=tk.W, padx=100)

        self.radio_var_two = StringVar(None)
        self.aes_radio_button_d = ttk.Radiobutton(self.decrypt_frame,
                                                  text='AES',
                                                  variable=self.radio_var_two,
                                                  value=3)
        self.aes_radio_button_d.grid(column=0, row=5, sticky=tk.W, padx=19)
        self.two_fish_radio_button_d = ttk.Radiobutton(self.decrypt_frame,
                                                       text='Twofish',
                                                       variable=self.radio_var_two,
                                                       value=4)
        self.two_fish_radio_button_d.grid(column=0, row=6, sticky=tk.W, padx=19)

        self.label_three = Label(
            self.decrypt_frame, text="3. Decryption")
        self.label_three.grid(column=0, row=7, sticky=tk.W, padx=5, pady=10)

        self.encrypted_file_var = StringVar(None)

        self.label_five = Label(
            self.decrypt_frame, text="Working Directory: ")
        self.label_five.grid(column=0, row=8, sticky=tk.W, padx=17, pady=5)

        self.decrypted_file_dir_var = StringVar(None)

        self.decrypted_file_path = ttk.Entry(
            self.decrypt_frame, width=44)

        self.decrypted_file_path.config(state=DISABLED)
        self.decrypted_file_path.place(x=150, y=238)

        self.encryption_photo = PhotoImage(
            file=r"icons\wicons8-password-50.png")
        self.encryption_photo_image = self.encryption_photo.subsample(3, 3)

        self.decrypt_button = ttk.Button(self.decrypt_frame,
                                         text="Decrypt", command=self.selected)
        self.decrypt_button.grid(column=0, row=9, sticky=tk.W, padx=19, pady=5)

    def open_original_file(self):

        self.file_types = (("All files", "*.*"), ("Text files", "*.txt*"))
        self.original_file = filedialog.askopenfilename(initialdir="/",
                                                        title="Choose a File",
                                                        filetypes=(("All files", "*.*"), ("Text files", "*.txt*")))

        self.original_file_path.set(self.original_file)
        self.original_file_entry.config(textvariable=self.original_file_path)

        shutil.copy(self.original_file, 'C:\Krypter\Files\original files')
        self.file_name = 'C:\Krypter\Files\original files\\' + \
                         os.path.basename(self.original_file)
        self.original_file_var.set(self.file_name)
        # self.encrypted_file_dest.config(textvariable=self.original_file_var)
        # if self.choose_button_one._name=="btn_one":
        #     self.original_file_var.set(self.file_name)
        # if self.choose_button_two._name=="btn_two":    
        #     self.encrypted_file_var.set(self.file_name)
        # print(self.file_name)

    def open_encrypted_file(self):
        self.file_types = (("All files", "*.*"), ("Text files", "*.txt*"))
        self.encrypted_file = filedialog.askopenfilename(initialdir="/",
                                                         title="Choose a File",
                                                         filetypes=(("All files", "*.*"), ("Text files", "*.txt*")))
        self.encrypted_file_var.set(self.encrypted_file)
        self.encrypted_file_entry.config(textvariable=self.encrypted_file_var)

        # shutil.copy(self.encrypted_file, 'C:\Krypter\Files\original files')
        # self.file_name = 'C:\Krypter\Files\original files\\' + \
        #                  os.path.basename(self.encrypted_file)

    def toggle_password(self):
        if self.password_entry.cget('show') == '':
            self.password_entry.config(show='*')
        else:
            self.password_entry.config(show='')

    def password_generator(self):
        self.lowercase_characters = string.ascii_lowercase
        self.uppercase_characters = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = string.punctuation

        self.all_characters = self.lowercase_characters + \
                              self.uppercase_characters + self.digits + self.symbols

        self.password_combo = random.sample(
            self.all_characters, MAX_PASSWORD_LENGTH)

        self.default_password = "".join(self.password_combo)
        self.default_password_var.set(self.default_password)

    def selected(self):

        # if self.encrypt_button["text"]=="Encrypt":
        if self.radio_var.get() == '1':
            self.encrypted_file_dir_var.set(self.aes_encrypted_path)
            aes_cipher(self.original_file, 'password').encrypt_file()
            self.encrypted_file_dest.config(textvariable=self.encrypted_file_dir_var)

        if self.radio_var.get() == '2':
            self.encrypted_file_dir_var.set(self.tf_encrypted_path)
            two_fish(self.original_file, 'password').encrypt_file()
            self.encrypted_file_dest.config(textvariable=self.encrypted_file_dir_var)

            # if self.decrypt_button["text"]=="Decrypt":
        # print(self.decrypt_button["text"])
        if self.radio_var_two.get() == '3':
            self.decrypted_file_dir_var.set(self.aes_decrypted_path)
            aes_cipher(self.encrypted_file, 'password').decrypt_file()
            self.decrypted_file_path.config(textvariable=self.decrypted_file_dir_var)
        if self.radio_var_two.get() == '4':
            self.decrypted_file_dir_var.set(self.tf_decrypted_path)
            two_fish(self.encrypted_file, 'password').decrypt_file()
            self.decrypted_file_path.config(textvariable=self.decrypted_file_dir_var)

    def change_to_encrypt(self):
        self.encrypt_frame.pack(fill="both", expand=True)
        self.decrypt_frame.forget()

    def change_to_decrypt(self):
        self.decrypt_frame.pack(fill="both", expand=True)
        self.encrypt_frame.forget()
        self.frame_var = self.frames[1]

        print("Hi")


if __name__ == '__main__':
    app = KrypterApp()
    app.mainloop()
