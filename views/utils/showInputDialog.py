import customtkinter as ctk
from tkinter import messagebox

def show_input_dialog(title: str, message: str) -> str | None:
    """
    Affiche une boîte de dialogue CTk pour saisir une valeur.
    Retourne la chaîne saisie, ou None si annulé.
    """
    result = {"value": None}

    # Création de la fenêtre
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.geometry("350x180")
    dialog.resizable(False, False)
    dialog.grab_set()  # bloque les interactions avec la fenêtre principale

    # Centrer la fenêtre
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) // 2
    y = (dialog.winfo_screenheight() - dialog.winfo_reqheight()) // 3
    dialog.geometry(f"+{x}+{y}")

    # Contenu
    frame = ctk.CTkFrame(dialog, corner_radius=12)
    frame.pack(expand=True, fill="both", padx=15, pady=15)

    ctk.CTkLabel(frame, text=message, wraplength=300, font=("Arial", 14)).pack(pady=(10, 10))

    entry = ctk.CTkEntry(frame, height=35, placeholder_text="Entrez une valeur ici...")
    entry.pack(pady=(0, 15), fill="x", padx=10)
    entry.focus_set()

    def on_ok():
        result["value"] = entry.get().strip()
        dialog.destroy()

    def on_cancel():
        result["value"] = None
        dialog.destroy()

    btn_frame = ctk.CTkFrame(frame)
    btn_frame.pack(pady=(5, 5))
    ctk.CTkButton(btn_frame, text="OK", command=on_ok, width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Annuler", command=on_cancel, width=100).pack(side="right", padx=5)

    dialog.wait_window()  # bloque jusqu’à fermeture
    return result["value"]