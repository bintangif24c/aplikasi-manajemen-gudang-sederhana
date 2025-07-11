import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
from collections import deque

produk_list = []
transaksi_queue = deque()

def load_data():
    try:
        with open('produk.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['harga'] = float(row['harga'])
                row['stok'] = int(row['stok'])
                produk_list.append(row)
    except FileNotFoundError:
        pass

def simpan_data():
    with open('produk.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['nama', 'harga', 'stok'])
        writer.writeheader()
        writer.writerows(produk_list)

def tambah_produk():
    nama = simpledialog.askstring("Input", "Nama produk:")
    harga = simpledialog.askfloat("Input", "Harga:")
    stok = simpledialog.askinteger("Input", "Stok:")

    if nama and harga is not None and stok is not None:
        produk_list.append({'nama': nama, 'harga': harga, 'stok': stok})
        simpan_data()
        messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")

def lihat_produk():
    win = tk.Toplevel(root)
    win.title("Daftar Produk Gudang")
    win.configure(bg="#f0f0f0")
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(frame, columns=("Nama", "Harga", "Stok"), show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("Nama", text="Nama Produk", anchor="center")
    tree.heading("Harga", text="Harga", anchor="center")
    tree.heading("Stok", text="Stok", anchor="center")

    tree.column("Nama", width=200, anchor="center")
    tree.column("Harga", width=100, anchor="center")
    tree.column("Stok", width=80, anchor="center")

    for p in produk_list:
        tree.insert("", "end", values=(p['nama'], f"Rp{p['harga']:,}", p['stok']))

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=tree.yview)

def tambah_transaksi(tipe):
    nama_produk = simpledialog.askstring("Input", "Nama produk:")
    jumlah = simpledialog.askinteger("Input", "Jumlah:")
    if not nama_produk or jumlah is None:
        return

    for p in produk_list:
        if p['nama'].lower() == nama_produk.lower():
            transaksi_queue.append({'tipe': tipe, 'produk': p, 'jumlah': jumlah})
            messagebox.showinfo("Sukses", f"Transaksi {tipe} ditambahkan ke antrian.")
            return
    messagebox.showerror("Error", "Produk tidak ditemukan!")

def proses_transaksi():
    if not transaksi_queue:
        messagebox.showinfo("Info", "Tidak ada transaksi dalam antrian.")
        return

    transaksi = transaksi_queue.popleft()
    produk = transaksi['produk']
    jumlah = transaksi['jumlah']
    tipe = transaksi['tipe']

    if tipe == 'Penjualan':
        if produk['stok'] >= jumlah:
            produk['stok'] -= jumlah
            messagebox.showinfo("Sukses", f"Penjualan {jumlah} unit {produk['nama']} diproses.")
        else:
            messagebox.showerror("Gagal", "Stok tidak cukup!")
            return
    elif tipe == 'Pembelian':
        produk['stok'] += jumlah
        messagebox.showinfo("Sukses", f"Pembelian {jumlah} unit {produk['nama']} diproses.")

    simpan_data()

def lihat_antrian():
    win = tk.Toplevel(root)
    win.title("Antrian Transaksi Gudang")
    win.configure(bg="#f0f0f0")
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(frame, columns=("Tipe", "Produk", "Jumlah"), show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("Tipe", text="Tipe Transaksi", anchor="center")
    tree.heading("Produk", text="Nama Produk", anchor="center")
    tree.heading("Jumlah", text="Jumlah", anchor="center")

    tree.column("Tipe", width=150, anchor="center")
    tree.column("Produk", width=200, anchor="center")
    tree.column("Jumlah", width=100, anchor="center")

    for transaksi in transaksi_queue:
        tree.insert("", "end", values=(transaksi['tipe'], transaksi['produk']['nama'], transaksi['jumlah']))

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=tree.yview)

root = tk.Tk()
root.title("Manajemen Gudang Sederhana")
root.configure(bg="#e0f7fa")  

judul = tk.Label(
    root,
    text="Manajemen Gudang Sederhana",
    font=("Segoe UI", 16, "bold"),
    bg="#e0f7fa",
    fg="#00796b"
)
judul.pack(pady=(15, 10))

button_styles = [
    {"bg": "#4dd0e1", "fg": "#fff", "activebackground": "#0097a7", "activeforeground": "#fff"},  
    {"bg": "#81c784", "fg": "#fff", "activebackground": "#388e3c", "activeforeground": "#fff"},  
    {"bg": "#ffb74d", "fg": "#fff", "activebackground": "#f57c00", "activeforeground": "#fff"},  
    {"bg": "#ba68c8", "fg": "#fff", "activebackground": "#6a1b9a", "activeforeground": "#fff"},  
    {"bg": "#e57373", "fg": "#fff", "activebackground": "#c62828", "activeforeground": "#fff"}, 
    {"bg": "#90caf9", "fg": "#1565c0", "activebackground": "#1976d2", "activeforeground": "#fff"},  
    {"bg": "#bdbdbd", "fg": "#212121", "activebackground": "#757575", "activeforeground": "#fff"},  
]

button_font = ("Segoe UI", 11)
button_bd = 0

tk.Button(
    root,
    text=" Tambah Produk",
    width=30,
    command=tambah_produk,
    font=button_font,
    bd=button_bd,
    **button_styles[0]
).pack(pady=5)

tk.Button(
    root,
    text=" Lihat Daftar Produk",
    width=30,
    command=lihat_produk,
    font=button_font,
    bd=button_bd,
    **button_styles[1]
).pack(pady=5)

tk.Button(
    root,
    text=" Tambah Transaksi Penjualan",
    width=30,
    command=lambda: tambah_transaksi('Penjualan'),
    font=button_font,
    bd=button_bd,
    **button_styles[2]
).pack(pady=5)

tk.Button(
    root,
    text=" Tambah Transaksi Pembelian",
    width=30,
    command=lambda: tambah_transaksi('Pembelian'),
    font=button_font,
    bd=button_bd,
    **button_styles[3]
).pack(pady=5)

tk.Button(
    root,
    text=" Proses Transaksi",
    width=30,
    command=proses_transaksi,
    font=button_font,
    bd=button_bd,
    **button_styles[4]
).pack(pady=5)

tk.Button(
    root,
    text=" Lihat Antrian Transaksi",
    width=30,
    command=lihat_antrian,
    font=button_font,
    bd=button_bd,
    **button_styles[5]
).pack(pady=5)

tk.Button(
    root,
    text=" Keluar",
    width=30,
    command=root.quit,
    font=button_font,
    bd=button_bd,
    **button_styles[6]
).pack(pady=(5, 15))

load_data()
root.mainloop()