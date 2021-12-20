# Line 2-6: Import modul yang diperlukan
from Crypto.Cipher import AES # Modul PyCryptodome untuk mengenkripsi dan dekripsi gambar menggunakan algoritma AES
import io # Modul I/O sebagai fasilitas utama yang mengatur berbagai jenis I/O (ada 3 tipe utama: text I/O, binary I/O, dan raw I/O)
import PIL.Image # Python Imaging Library bisa menambahkan banyak fitur pemrosesan file gambar ke Python
from tkinter import * # tkinter adalah standard GUI (Graphical User Interface) Python atau kotak layar yang muncul saat di run
import os # Modul OS ini dapat membuat program yang dikerjakan bisa cross-platform (dari Windows, Mac, atau Linux)

# Line 9-10: Inisialisasi variabel kunci (key dan iv ini required/wajib diperlukan agar terlindungi dan aman)
key = b'Key of length 16' # Untuk generate kunci secara acak (key size = 16 bytes * 8 = 128 bits)
iv = b'ivb of length 16' # Untuk inisialisasi Vektor (IV) secara acak (block sizenya juga 16 bytes/128 bits)


#Line 14-36: Program Enkripsi Gambar
def enkripsi_gambar():
    global key,iv,entry_for_folder
    file_path=str(entry_for_folder.get()) # Get/Mengambil path/direktori file pada folder yang dituju
    if(file_path=="" or file_path[0]==" "): # Jika isinya kosong,
        file_path=os.getcwd() # maka tidak akan menampilkan apa-apa dan dengan method .getcwd akan memberi tahu system bahwa "Current Working Directory atau direktori sedang dalam pengerjaan"
    files=[]

    # Keterangan: r = root, d = directory, f = file, rb = read binary, cfb = ciphertext feedback, wb = write bytes
    for r, d, f in os.walk(file_path): # os.walk untuk menghasilkan nama file dari file_path
        for file in f:
            if((('.png' in file) or ('.jpg' in file)) and ('.enkripsi' not in file)): # Jika file .png atau .jpg ada dalam folder dan tidak ada file .enkripsi,
                files.append(os.path.join(r, file)) # maka file-file yang ada akan ditambahkan ke dalam sistem, lalu bergabung dengan path dari file r (root)
    for file_name in files:
        input_file = open(file_name,"rb") # Buka file sebagai read-only pada format binary
        input_data = input_file.read() # Baca data yang di input
        input_file.close()

        cfb_cipher = AES.new(key, AES.MODE_CFB, iv) # Buat sebuah objek cipher AES dengan kunci dan IV menggunakan mode CFB
        enkripsi_data = cfb_cipher.encrypt(input_data) # Masukkan data lalu enkripsi

        enkripsi_file = open(file_name+".enkripsi", "wb") # File-file gambar yang sudah dienkripsi akan memiliki penamaan "nama_file.enkripsi"
        enkripsi_file.write(enkripsi_data) # Penulisan ciphertext yang panjang ke dalam file (inilah isi file enkripsinya)
        enkripsi_file.close()


# Line 40-65: Program Dekripsi Gambar
def dekripsi_gambar():
    global key,iv,entry_for_folder
    file_path = str(entry_for_folder.get()) # Get/Mengambil path/direktori file pada folder yang dituju
    if (file_path == "" or file_path[0] == " "): # Jika isinya kosong,
        file_path = os.getcwd() # maka tidak akan menampilkan apa-apa dan dengan method .getcwd akan memberi tahu system bahwa "Current Working Directory atau direktori sedang dalam pengerjaan"
    files = []
    
    # Keterangan: r = root, d = directory, f = file, rb = read binary, cfb = ciphertext feedback
    for r, d, f in os.walk(file_path): # os.walk untuk menghasilkan nama file dari file_path
        for file in f:
            if '.enkripsi' in file: # Jika terdapat file .enkripsi,
                files.append(os.path.join(r, file)) # maka file-file yang ada akan ditambahkan ke dalam sistem, lalu bergabung dengan path dari file r (root)
    for file_name in files:
        enkripsi_file2 = open(file_name,"rb") # Buka file sebagai read-only pada format binary
        enkripsi_data2 = enkripsi_file2.read() # Baca enkripsi data yang ada pada folder
        enkripsi_file2.close()

        cfb_decipher = AES.new(key, AES.MODE_CFB, iv) # Buat sebuah objek cipher AES dengan kunci dan IV menggunakan mode CFB
        plain_data = (cfb_decipher.decrypt(enkripsi_data2)) # Dekripsi file-file yang di enkripsi pada folder yang sama

        imageStream = io.BytesIO(plain_data)
        imageFile = PIL.Image.open(imageStream) # Proses membuka banyak file gambar dalam satu folder
        if('.jpg' in file_name): # Jika file .jpg,
            imageFile.save((file_name[:-8])+"dekripsi"+".jpg") # maka penamaan file yang telah di dekripsi adalah "nama_file.dekripsi.jpg"
        elif('.png' in file_name): # Jika file .png
            imageFile.save((file_name[:-8])+"dekripsi"+".png") # maka penamaan file yang telah di dekripsi adalah "nama_file.dekripsi.png"


# Line 70-90: Tkinter Window
root = Tk()

root.title("AES-128 Enkripsi & Dekripsi Gambar JPG & PNG - V3920057 - Tanzil R.K.") # Judul pada tkinter GUI

# Line 74-81: Untuk input folder gambar dan di enkripsi
folder_directory_label = Label(text = "Masukkan Path/Direktori Folder Gambar")
folder_directory_label.pack()

entry_for_folder = Entry(root)
entry_for_folder.pack()

encrypt = Button(text = "Enkripsi",command = enkripsi_gambar) # Tombol enkripsi folder dengan menjalankan fungsi enkripsi_gambar
encrypt.pack()

# Line 84-87: Untuk dekripsi file-file gambar
label = Label(text = "Sebelum folder di dekripsi, hapus semua file gambar yang sudah terenkripsi!")
label.pack()

decrypt = Button(text = "Dekripsi",command = dekripsi_gambar) # Tombol dekripsi folder dengan menjalankan fungsi dekripsi_gambar
decrypt.pack()

root.mainloop() # Looping