import tkinter as tk
from PIL import Image, ImageTk
import glob
import itertools

def show_downloaded_images(root):
    image_window = tk.Toplevel(root)
    image_window.title("İndirilen Görseller")
    image_window.geometry("600x400")

    canvas = tk.Canvas(image_window)
    scrollbar = tk.Scrollbar(image_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 🔥 Tüm görsel uzantılarını tara
    image_files = list(itertools.chain.from_iterable([
        glob.glob("data/*.jpg"),
        glob.glob("data/*.jpeg"),
        glob.glob("data/*.png")
    ]))

    row = 0
    col = 0

    for image_path in image_files:
        try:
            img = Image.open(image_path)
            img.thumbnail((120, 120))
            photo = ImageTk.PhotoImage(img)

            lbl = tk.Label(scrollable_frame, image=photo)
            lbl.image = photo
            lbl.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col > 4:
                col = 0
                row += 1
        except Exception as e:
            print(f"⚠️ Görsel gösterilemedi: {image_path}", e)
            continue
