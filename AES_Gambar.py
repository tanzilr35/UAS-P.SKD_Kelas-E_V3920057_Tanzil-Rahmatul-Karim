# Line 2-6: Import modul yang diperlukan
from Crypto.Cipher import AES
import io
import PIL.Image
from tkinter import *
import os

# Line 9-10: Inisialisasi variabel kunci (Kedua kunci ini (Key1 dan Key2) di required agar aman)
key = b'Key of length 16' # Untuk memasukkan sebuah key1
iv = b'ivb of length 16' # Untuk memasukkan sebuah ivb


#Line 14-36: Program Enkripsi Gambar
def enkripsi_gambar():
    global key,iv,entry_for_folder
    file_path=str(entry_for_folder.get())
    if(file_path=="" or file_path[0]==" "):
        file_path=os.getcwd()
    files=[]

    # Keterangan: r = root, d = directories, f = files
    for r, d, f in os.walk(file_path):
        for file in f:
            if((('.png' in file) or ('.jpg' in file)) and ('.enkripsi' not in file)):
                files.append(os.path.join(r, file))
    for file_name in files:
        input_file = open(file_name,"rb")
        input_data = input_file.read()
        input_file.close()

        cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
        enkripsi_data = cfb_cipher.encrypt(input_data)

        enkripsi_file = open(file_name+".enkripsi", "wb")
        enkripsi_file.write(enkripsi_data)
        enkripsi_file.close()


# Line 40-64: Program Dekripsi Gambar
def dekripsi_gambar():
    global key,iv,entry_for_folder
    file_path = str(entry_for_folder.get())
    if (file_path == "" or file_path[0] == " "):
        file_path = os.getcwd()
    files = []
    
    # Keterangan: r = root, d = directories, f = files
    for r, d, f in os.walk(file_path):
        for file in f:
            if '.enkripsi' in file:
                files.append(os.path.join(r, file))
    for file_name in files:
        enkripsi_file2 = open(file_name,"rb")
        enkripsi_data2 = enkripsi_file2.read()
        enkripsi_file2.close()

        cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
        plain_data = (cfb_decipher.decrypt(enkripsi_data2))

        imageStream = io.BytesIO(plain_data)
        imageFile = PIL.Image.open(imageStream)
        if('.jpg' in file_name):
            imageFile.save((file_name[:-8])+"dekripsi"+".jpg")
        elif('.png' in file_name):
            imageFile.save((file_name[:-8])+"dekripsi"+".png")


# Line 70-90: Tkinter Window
root=Tk()

root.title("AES-128 Enkripsi & Dekripsi Gambar JPG & PNG - V3920057 - Tanzil R.K.") # Judul pada tkinter window

# Line 74-81: Untuk input folder gambar dan di enkripsi
folder_directory_label = Label(text = "Masukkan Path/Direktori Folder Gambar")
folder_directory_label.pack()

entry_for_folder = Entry(root)
entry_for_folder.pack()

encrypt = Button(text = "Enkripsi",command = enkripsi_gambar) # Tombol enkripsi folder
encrypt.pack()

# Line 84-87: Untuk dekripsi file-file gambar
label = Label(text = "Sebelum folder di dekripsi, hapus semua file gambar yang sudah terenkripsi!")
label.pack()

decrypt = Button(text = "Dekripsi",command = dekripsi_gambar) # Tombol dekripsi folder
decrypt.pack()

root.mainloop() # Looping