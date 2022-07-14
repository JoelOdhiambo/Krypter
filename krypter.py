import os
import filecmp
import shutil
from functools import partial
import tkinter as tk
from tkinter import BOTTOM, DISABLED, GROOVE, SUNKEN, Entry, Label, Menu, PhotoImage, Radiobutton, StringVar, ttk
from tkinter import filedialog

import random
import string
from colorama import Style

from torch import var

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__),'..','ciphers'))
from ciphers.aes import AesCipher as aes_cipher
from ciphers.twofish_cipher import TwofishCipher as two_fish

MAX_PASSWORD_LENGTH = 16


class KrypterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # try:
        #     self.working_directory="Files"
        #     self.parent_directory="C:/Krypter/"
        #     self.app_path=os.path.join(self.parent_directory, self.working_directory)
        #     os.mkdir(self.app_path)
        # except:
        #     print("Directory Exists")

        self.app_dir = 'C:/Krypter/Files'
        
        list=('original files','encrypted files/AES','encrypted files/Two fish')

        app_path=partial(os.path.join,self.app_dir)
        make_directory=partial(os.makedirs, exist_ok=True)
        
        for directories in map(app_path,list):
            make_directory(directories)
            
        # if not os.path.exists(self.app_dir):
        #     os.makedirs(self.app_dir)
        # else:
        #     print("Directory Exists")

        self.title('Krypter')
        self.tk.call('wm', 'iconphoto', self._w,
                     tk.PhotoImage(file='icons\Krypter Icon.png'))
        self.geometry('500x500')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(
            label="Open",
            command=self.open_file
        )

        self.file_menu.add_separator()
        self.sub_menu = Menu(self.file_menu, tearoff=0)
        self.sub_menu.add_command(label='Toggle Dark Mode')
        self.file_menu.add_cascade(
            label="Preferences",
            menu=self.sub_menu
        )
        self.file_menu.add_separator()

        self.file_menu.add_command(
            label="Quit",
            command=self.destroy
        )

        self.menu_bar.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0
        )

        self.label_one = Label(self, text="1. Choose file to encrypt")
        self.label_one.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # self.separator_two=ttk.Separator(self,orient='horizontal')
        # self.separator_two.place(relx=0,rely=0.1,relheight=0.5,relwidth=1)

        self.path_name = StringVar(None)

        self.file_path_box = ttk.Entry(
            self, textvariable=self.path_name, width=44)
        self.file_path_box.grid(column=0, row=1, sticky=tk.W, padx=20, pady=5)

        self.choose_button = ttk.Button(
            text="Choose File", command=self.open_file)
        self.choose_button.grid(column=1, row=1, sticky=tk.W, pady=5)

        self.label_two = Label(
            self, text="2. Enter a password and choose an Encryption Algorithm")
        self.label_two.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        # self.separator_two=ttk.Separator(self,orient='horizontal')
        # self.separator_two.place(relx=0,rely=0.3,relheight=0.5,relwidth=1)

        # self.password_label=Label(self, text='Password')
        # self.password_label.grid(column=0, row=3, sticky=tk.W,padx=17)
        self.default_password_var = tk.StringVar(None)

        self.password_entry = ttk.Entry(
            self, textvariable=self.default_password_var, width=44)
        self.password_entry.grid(column=0, row=3, sticky=tk.W, padx=20, pady=5)

        self.generate_button = ttk.Button(
            text="Generate Password", command=self.password_generator)
        self.generate_button.grid(column=1, row=3, sticky=tk.W, pady=5)

        self.check_button = ttk.Checkbutton(
            self, text="Hide Password", onvalue=False, offvalue=True, command=self.toggle_password)

        self.check_button.grid(column=0, row=4, sticky=tk.W, padx=100)

        self.radio_var = StringVar(None)
        self.aes_radio_button = ttk.Radiobutton(text='AES',
                                                variable=self.radio_var,
                                                value=1)
        self.aes_radio_button.grid(column=0, row=5, sticky=tk.W, padx=19)
        self.two_fish_radio_button = ttk.Radiobutton(text='Two Fish',
                                                     variable=self.radio_var,
                                                     value=2)
        self.two_fish_radio_button.grid(column=0, row=6, sticky=tk.W, padx=19)

        self.label_three = Label(
            self, text="3. Encryption")
        self.label_three.grid(column=0, row=7, sticky=tk.W, padx=5, pady=10)

        self.label_four = Label(
            self, text="Working Directory: ")
        self.label_four.grid(column=0, row=8, sticky=tk.W, padx=17, pady=5)

        self.app_directory_var = StringVar(None)
        
        
        self.app_directory_entry = ttk.Entry(
            self, textvariable=self.app_directory_var, width=44)
        
        self.app_directory_entry.config(state=DISABLED)
        self.app_directory_entry.place(x=130,y=242)

        self.encryption_photo = PhotoImage(
            file=r"icons\wicons8-password-50.png")
        self.encryption_photo_image = self.encryption_photo.subsample(3, 3)

        self.encrypt_button = ttk.Button(
            text="Encrypt", command=self.selected)
        self.encrypt_button.grid(column=0, row=9, sticky=tk.W, padx=19, pady=5)


        self.separator_two=ttk.Separator(self,orient='horizontal')
        self.separator_two.place(relx=0,rely=0.95,relheight=0.5,relwidth=1)

        # self.progress_bar=ttk.Progressbar(self,orient='horizontal',mode='indeterminate',length=100)
        # self.progress_bar.place(x=1,y=453)
        
    def open_file(self):
        
        self.file_types = (("Text files", "*.txt*"), ("All files", "*.*"))
        self.selected_file = filedialog.askopenfilename(initialdir="/",
                                                    title="Choose a File",
                                                    filetypes=(("Text files", "*.txt*"), ("All files", "*.*")))
        self.path_name.set(self.selected_file)
        shutil.copy(self.selected_file,'C:\Krypter\Files\original files')
        self.file_name='C:\Krypter\Files\original files\\'+os.path.basename(self.selected_file)
        self.app_directory_var.set(self.file_name)
        print( self.file_name)

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
       
        if self.radio_var.get() =='1':
            aes_cipher(self.file_name,'password').encrypt_file()
            
        if self.radio_var.get()=='2':
            two_fish(self.file_name,'password').encrypt_file()
            print("Two Fish")
       
if __name__ == '__main__':

    app = KrypterApp()
    app.mainloop()
