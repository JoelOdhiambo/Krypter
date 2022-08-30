import os
import shutil
import random
import string
import time
import tkinter as tk
import threading
import ciphers.twofish_cipher

from functools import partial
from tkinter import Frame, Label, PhotoImage, StringVar, ttk
from tkinter import filedialog

from ciphers.aes_cipher import AesCipher as aes_cipher
from ciphers.twofish_cipher import TwofishCipher as two_fish

MAX_PASSWORD_LENGTH = 16


class KrypterApp(tk.Tk, ciphers.twofish_cipher.TwofishCipher, ciphers.aes_cipher.AesCipher):
    def __init__(self):
        super().__init__()

        # Krypter directory structure
        self.app_dir = 'C:/Krypter/Files'

        sub_directory_tree = ('original files', 'encrypted files/AES',
                              'encrypted files/Twofish', 'decrypted files/AES', 'decrypted files/Twofish')

        app_path = partial(os.path.join, self.app_dir)
        make_directory = partial(os.makedirs, exist_ok=True)

        for directories in map(app_path, sub_directory_tree):
            make_directory(directories)

        self.title('Krypter')
        # GUI icon
        self.tk.call('wm', 'iconphoto', self._w,
                     tk.PhotoImage(file='icons\Krypter Icon.png'))
        self.geometry('500x500')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # self.menu_bar = Menu(self)
        #
        # self.config(menu=self.menu_bar)
        #
        # self.file_menu = Menu(self.menu_bar, tearoff=0)
        # self.file_menu.add_command(
        #     label="Open",
        #     command=self.open_file
        # )
        #
        # self.file_menu.add_separator()
        #
        # self.sub_menu = Menu(self.file_menu, tearoff=0)
        #
        # self.sub_menu.add_command(label='Toggle Dark Mode')
        # self.file_menu.add_cascade(
        #     label="Preferences",
        #     menu=self.sub_menu
        # )
        #
        # self.file_menu.add_separator()
        #
        # self.file_menu.add_command(
        #     label="Quit",
        #     command=self.destroy
        # )
        #
        # self.menu_bar.add_cascade(
        #     label="File",
        #     menu=self.file_menu,
        #     underline=0
        # )
        #
        # self.encrypt_menu = Menu(self.menu_bar, tearoff=0)
        #
        # self.menu_bar.add_cascade(
        #     label="Encrypt",
        #     menu=self.encrypt_menu,
        #     command=self.change_to_encrypt
        #
        # )
        #
        # self.decrypt_menu = Menu(self.menu_bar, tearoff=0)
        #
        # self.menu_bar.add_cascade(
        #     label="Decrypt",
        #     menu=self.decrypt_menu,
        #     command=self.change_to_decrypt
        # )

        # Create a notebook to display the Encryption and Decryption Frames
        self.notebook = ttk.Notebook(self)

        self.encrypt_frame = Frame(self.notebook)

        self.decrypt_frame = Frame(self.notebook)

        self.notebook.pack(expand=1, fill="both")

        self.notebook.add(self.encrypt_frame, text="Encrypt")
        self.notebook.add(self.decrypt_frame, text="Decrypt")

        """
        Encryption Frame
        # Here we build a frame that will be part of the GUI where the user can encrypt files
        """

        self.label_choose = Label(
            self.encrypt_frame, text="1. Choose file to encrypt")
        self.label_choose.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # Path Variable for original file
        self.original_file_path = StringVar(None)

        self.original_file_entry = ttk.Entry(
            self.encrypt_frame, width=44, state='disabled')
        self.original_file_entry.grid(
            column=0, row=1, sticky=tk.W, padx=20, pady=5)

        self.bool_one = StringVar(None)
        self.choose_button_one = ttk.Button(self.encrypt_frame,
                                            text="Choose File", name="btn_one", command=self.open_original_file)
        self.choose_button_one.grid(column=1, row=1, sticky=tk.W, pady=5)

        self.label_two = Label(
            self.encrypt_frame, text="2. Enter a password and choose an Encryption Algorithm")
        self.label_two.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.default_password_var = tk.StringVar(None)
        self.default_password_var.set("password")
        self.password_entry_one = ttk.Entry(
            self.encrypt_frame, textvariable=self.default_password_var, width=44)
        self.password_entry_one.grid(
            column=0, row=3, sticky=tk.W, padx=20, pady=5)

        self.generate_button = ttk.Button(self.encrypt_frame,
                                          text="Generate Password", command=self.generate_password)
        self.generate_button.grid(column=1, row=3, sticky=tk.W, pady=5)

        self.check_button_one = ttk.Checkbutton(
            self.encrypt_frame, text="Hide Password", onvalue=False, offvalue=True, command=self.toggle_password)

        self.check_button_one.grid(column=0, row=4, sticky=tk.W, padx=100)

        # Radiobutton variable ('self.radio_var' below and 'self.radio_var_two' in Decryption Frame) to store the
        # state of radiobuttons '0' for None are active_radio_button '1' for AES Encryption '2' for Twofish
        # Encryption '3' for AES Decryption '4' for Twofish Decryption.
        self.radio_var = StringVar(None)
        self.radio_var.set('0')

        self.aes_radio_button_e = ttk.Radiobutton(self.encrypt_frame,
                                                  text='AES',
                                                  variable=self.radio_var,
                                                  state='disabled',
                                                  value=1,
                                                  command=self.radio_button_state)
        self.aes_radio_button_e.grid(column=0, row=5, sticky=tk.W, padx=19)
        self.two_fish_radio_button_e = ttk.Radiobutton(self.encrypt_frame,
                                                       text='Twofish',
                                                       variable=self.radio_var,
                                                       state='disabled',
                                                       value=2,
                                                       command=self.radio_button_state)
        self.two_fish_radio_button_e.grid(
            column=0, row=6, sticky=tk.W, padx=19)

        self.label_three = Label(
            self.encrypt_frame, text="3. Encryption")
        self.label_three.grid(column=0, row=7, sticky=tk.W, padx=5, pady=10)

        # Path variable for encrypted files
        self.encrypted_file_dir_var = StringVar(None)

        self.label_four = Label(
            self.encrypt_frame, text="Working Directory: ")
        self.label_four.grid(column=0, row=8, sticky=tk.W, padx=17, pady=5)

        self.original_file_var = StringVar(None)

        self.encrypted_file_dest = ttk.Entry(
            self.encrypt_frame, width=44)

        self.encrypted_file_dest.config(state='disabled')
        self.encrypted_file_dest.place(x=130, y=242)

        self.encryption_photo = PhotoImage(
            file=r"icons\wicons8-password-50.png")
        self.encryption_photo_image = self.encryption_photo.subsample(3, 3)

        self.encrypt_button = ttk.Button(self.encrypt_frame,
                                         text="Encrypt", command=self.run_thread, state='disabled')
        self.encrypt_button.grid(column=0, row=9, sticky=tk.W, padx=19, pady=5)

        self.view_encrypted_file_button = ttk.Button(self.encrypt_frame,
                                           text="View file", command=self.open_encrypted_file, state='disabled')
        self.view_encrypted_file_button.grid(
            column=0, row=9, sticky=tk.W, padx=115, pady=5)

        """
        Decryption Frame
        # Here we build a frame that will be part of the GUI where the user can decrypt files
        """

        self.label_choose_d = Label(
            self.decrypt_frame, text="1. Choose file to decrypt")
        self.label_choose_d.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # Path variable of the encrypted file
        self.encrypted_file_path = StringVar(None)

        self.encrypted_file_entry = ttk.Entry(
            self.decrypt_frame, width=44, state = 'disabled')
        self.encrypted_file_entry.grid(
            column=0, row=1, sticky=tk.W, padx=20, pady=5)

        self.bool_two = StringVar(None)
        self.choose_button_two = ttk.Button(self.decrypt_frame,
                                            text="Choose File ", name="btn_two", command=self.open_encrypted_file)
        self.choose_button_two.grid(column=1, row=1, sticky=tk.W, pady=5)

        self.label_two = Label(
            self.decrypt_frame, text="2. Enter your password and choose a Decryption Algorithm")
        self.label_two.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.password_entry_two = ttk.Entry(
            self.decrypt_frame, width=44)
        self.password_entry_two.grid(
            column=0, row=3, sticky=tk.W, padx=20, pady=5)

        self.check_button_two = ttk.Checkbutton(
            self.decrypt_frame, text="Hide Password", onvalue=False, offvalue=True, command=self.toggle_password)

        self.check_button_two.grid(column=0, row=4, sticky=tk.W, padx=100)

        self.radio_var_two = StringVar(None)
        self.radio_var_two.set('0')

        self.aes_radio_button_d = ttk.Radiobutton(self.decrypt_frame,
                                                  text='AES',
                                                  state='disabled',
                                                  variable=self.radio_var_two,
                                                  value=3,
                                                  command=self.radio_button_state)
        self.aes_radio_button_d.grid(column=0, row=5, sticky=tk.W, padx=19)
        self.two_fish_radio_button_d = ttk.Radiobutton(self.decrypt_frame,
                                                       text='Twofish',
                                                       state='disabled',
                                                       variable=self.radio_var_two,
                                                       value=4,
                                                       command=self.radio_button_state)
        self.two_fish_radio_button_d.grid(
            column=0, row=6, sticky=tk.W, padx=19)

        self.label_three = Label(
            self.decrypt_frame, text="3. Decryption")
        self.label_three.grid(column=0, row=7, sticky=tk.W, padx=5, pady=10)

        self.encrypted_file_var = StringVar(None)

        self.label_five = Label(
            self.decrypt_frame, text="Working Directory: ")
        self.label_five.grid(column=0, row=8, sticky=tk.W, padx=17, pady=5)

        # Path variable for decrypted files
        self.decrypted_file_dir_var = StringVar(None)

        self.decrypted_file_path = ttk.Entry(
            self.decrypt_frame, width=44)

        self.decrypted_file_path.config(state='disabled')
        self.decrypted_file_path.place(x=150, y=238)

        self.encryption_photo = PhotoImage(
            file=r"icons\wicons8-password-50.png")
        self.encryption_photo_image = self.encryption_photo.subsample(3, 3)

        self.decrypt_button = ttk.Button(self.decrypt_frame,
                                         text="Decrypt", state='disabled', command=self.run_thread)
        self.decrypt_button.grid(column=0, row=9, sticky=tk.W, padx=19, pady=5)

        self.view_decrypted_file_button = ttk.Button(self.decrypt_frame,
                                                     text="View file", command=self.open_decrypted_file,
                                                     state='disabled')
        self.view_decrypted_file_button.grid(
            column=0, row=9, sticky=tk.W, padx=115, pady=5)

        self.status_bar = ttk.Label(self, text=" Waiting... ", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.progress_bar = ttk.Progressbar(
            self.status_bar, orient='horizontal', mode='indeterminate', length=100)
        self.progress_bar.grid(column=3, row=3, columnspan=2, padx=390, pady=4)

        # self.progress_bar_text = ttk.Label(self, text="Waiting", background='')
        # self.progress_bar_text.place(x=329, y=475)

    def open_original_file(self):
        # print(list(self.encrypt_button.state())[0])
        # if list(self.encrypt_button.state())[0] != "enabled":
        #     self.encrypt_button.config(state='disabled')

        self.file_types = (("All files", "*.*"), ("Text files", "*.txt*"))
        self.original_file = filedialog.askopenfilename(initialdir="/",
                                                        title="Choose a File",
                                                        filetypes=(("All files", "*.*"), ("Text files", "*.txt*")))

        self.original_file_path.set(self.original_file)
        self.original_file_entry.config(textvariable=self.original_file_path)
        print(self.original_file_entry.get())
        print("Hi" + self.original_file)
        shutil.copy(self.original_file, 'C:\Krypter\Files\original files')
        self.file_name = 'C:\Krypter\Files\original files\\' + \
                         os.path.basename(self.original_file)
        self.original_file_var.set(self.file_name)

        self.aes_radio_button_e.config(state="active")
        self.two_fish_radio_button_e.config(state="active")
        if 'disabled' not in self.view_encrypted_file_button.state():
            self.view_encrypted_file_button.config(state='disabled')

    def open_encrypted_file(self):
        self.file_types = (("All files", "*.*"), ("Text files", "*.txt*"))
        self.encrypted_file = filedialog.askopenfilename(initialdir="C:/Krypter/Files/encrypted files",
                                                         title="Choose a File",
                                                         filetypes=(("All files", "*.*"), ("Text files", "*.txt*")))
        self.encrypted_file_var.set(self.encrypted_file)
        self.encrypted_file_entry.config(textvariable=self.encrypted_file_var)

        self.aes_radio_button_d.config(state="active")
        self.two_fish_radio_button_d.config(state="active")
        if 'disabled' not in self.view_decrypted_file_button.state():
            self.view_decrypted_file_button.config(state='disabled')

    def open_decrypted_file(self):
        self.file_types = (("All files", "*.*"), ("Text files", "*.txt*"))
        self.encrypted_file = filedialog.askopenfilename(initialdir=self.decrypted_file_dir_var.get(),
                                                         title="Choose a File",
                                                         filetypes=(("All files", "*.*"), ("Text files", "*.txt*")))
        self.encrypted_file_var.set(self.encrypted_file)
        self.encrypted_file_entry.config(textvariable=self.encrypted_file_var)

    def toggle_password(self):
        if self.password_entry_one.cget('show') == '':
            self.password_entry_one.config(show='*')
            self.check_button_one.config(text="Show Password")
        else:
            self.password_entry_one.config(show='')
            self.check_button_one.config(text="Hide Password")

        if self.password_entry_two.cget('show') == '':
            self.password_entry_two.config(show='*')
            self.check_button_two.config(text="Show Password")
        else:
            self.password_entry_two.config(show='')
            self.check_button_two.config(text="Hide Password")

    def generate_password(self):
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

    def radio_button_state(self):
        if 'active' in self.aes_radio_button_e.state() or self.two_fish_radio_button_e.state():
            self.encrypt_button.config(state='enabled')

        if 'active' in self.aes_radio_button_d.state() or self.two_fish_radio_button_d.state():
            self.decrypt_button.config(state='enabled')

    def run_thread(self):
        execute_thread = threading.Thread(target=self.active_radio_button)
        execute_thread.start()

    def active_radio_button(self):

        self.progress_bar.start(10)

        if self.radio_var.get() and self.radio_var_two.get() == 0:
            print("Choose and algorithm")

        if 'active' in self.encrypt_button.state():
            if self.radio_var.get() == '1':
                self.status_bar.config(text="  AES encryption in progress...")
                self.encrypted_file_dir_var.set(self.aes_encrypted_path)
                aes_cipher(self.original_file,
                           self.password_entry_one.get()).encrypt_file()
                self.encrypted_file_dest.config(
                    textvariable=self.encrypted_file_dir_var)

            if self.radio_var.get() == '2':
                self.status_bar.config(text="  Twofish encryption in progress...")
                self.encrypted_file_dir_var.set(self.tf_encrypted_path)
                two_fish(self.original_file,
                         self.password_entry_one.get()).encrypt_file()
                self.encrypted_file_dest.config(
                    textvariable=self.encrypted_file_dir_var)
            self.view_encrypted_file_button.config(state='normal')
            self.encrypt_button.config(state='disabled')

        if 'active' in self.decrypt_button.state():
            if self.radio_var_two.get() == '3':
                self.status_bar.config(text="  AES decryption in progress...")
                self.decrypted_file_dir_var.set(self.aes_decrypted_path)
                aes_cipher(self.encrypted_file,
                           self.password_entry_two.get()).decrypt_file()
                self.decrypted_file_path.config(
                    textvariable=self.decrypted_file_dir_var)

            if self.radio_var_two.get() == '4':
                self.status_bar.config(text="  Twofish decryption in progress...")
                self.decrypted_file_dir_var.set(self.tf_decrypted_path)
                two_fish(self.encrypted_file,
                         self.password_entry_two.get()).decrypt_file()
                self.decrypted_file_path.config(
                    textvariable=self.decrypted_file_dir_var)
            self.view_decrypted_file_button.config(state='normal')
            self.decrypt_button.config(state='disabled')

        time.sleep(1)
        self.status_bar.config(text=" File Encrypted!")
        time.sleep(1)
        self.status_bar.config(text=" Waiting...")
        self.progress_bar.stop()

    def is_clicked(self):
        print(self.decrypt_button.state())
    def change_to_encrypt(self):
        self.encrypt_frame.pack(fill="both", expand=True)
        self.decrypt_frame.forget()

    def change_to_decrypt(self):
        self.decrypt_frame.pack(fill="both", expand=True)
        self.encrypt_frame.forget()
        self.frame_var = self.frames[1]


if __name__ == '__main__':
    app = KrypterApp()
    app.mainloop()
