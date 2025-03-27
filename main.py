import tkinter as tk
from tkinter import ttk, messagebox
from scraper.core import start_scraping
from scraper.helpers import is_valid_url
from ui.input_section import create_input_section
from ui.result_gallery import show_downloaded_images

root = tk.Tk()
root.title("Web Kazıyıcı")
root.geometry("400x200")

url_var = tk.StringVar()
data_type_var = tk.StringVar(value="images")

create_input_section(root, url_var, data_type_var)

def on_start():
    url = url_var.get()
    data_type = data_type_var.get()

    if not url:
        messagebox.showerror("Hata", "Lütfen bir URL giriniz.")
        return

    if not is_valid_url(url):
        messagebox.showerror("Hatalı URL", "Geçerli bir URL giriniz.")
        return

    try:
        result = start_scraping(url, data_type)
        if result == 0:
            messagebox.showinfo("Sonuç", "Hiç veri bulunamadı.")
            return

        messagebox.showinfo("Başarılı", f"{result} veri indirildi.")
        if data_type == "images":
            show_downloaded_images(root)
    except Exception as e:
        messagebox.showerror("Hata", str(e))

tk.Button(root, text="Başlat", command=on_start).pack(pady=15)
root.mainloop()
