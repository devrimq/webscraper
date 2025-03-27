import tkinter as tk
from tkinter import ttk

def create_input_section(root, url_var, data_type_var):
    tk.Label(root, text="Web Sitesi URL:").pack(pady=5)
    url_entry = tk.Entry(root, textvariable=url_var, width=50)
    url_entry.pack(pady=5)

    tk.Label(root, text="Kazınacak Veri Türü:").pack(pady=5)
    ttk.Combobox(
        root,
        textvariable=data_type_var,
        values=["images", "titles", "links"]
    ).pack(pady=5)

    return url_entry
