import customtkinter as ctk
from tkinter import messagebox

def clear_root(root):
    """Efface tout le contenu de la fenêtre."""
    for widget in root.winfo_children():
        widget.destroy()


def show_custom_message(title, message, type_="info", parent=None):
    """Affiche une notification toast avec options épingler/fermer."""
    colors = {
        "info": "#3B82F6",
        "success": "#22C55E",
        "warning": "#EAB308",
        "error": "#EF4444",
    }
    color = colors.get(type_, "#3B82F6")

    toast = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
    toast.place(relx=0.5, rely=0.95, anchor="s")

    is_pinned = ctk.BooleanVar(value=False)

    def close_toast():
        toast.destroy()

    def toggle_pin():
        is_pinned.set(not is_pinned.get())
        if is_pinned.get():
            pin_button.configure(text="📌", fg_color="#1E3A8A")
        else:
            pin_button.configure(text="📍", fg_color=color)
            toast.after(3000, lambda: toast.destroy() if not is_pinned.get() else None)

    header = ctk.CTkFrame(toast, fg_color="transparent")
    header.pack(fill="x", padx=5, pady=(5, 0))

    ctk.CTkLabel(header, text=title, font=("Arial", 14, "bold"),
                 text_color="white", anchor="w").pack(side="left", padx=(8, 0))

    pin_button = ctk.CTkButton(header, text="📍", width=28, height=24,
                               corner_radius=8, fg_color=color, hover_color="#1E3A8A",
                               text_color="white", font=("Arial", 13),
                               command=toggle_pin)
    pin_button.pack(side="right", padx=(0, 3))

    close_button = ctk.CTkButton(header, text="✖", width=28, height=24,
                                 corner_radius=8, fg_color=color, hover_color="#991B1B",
                                 text_color="white", font=("Arial", 13, "bold"),
                                 command=close_toast)
    close_button.pack(side="right", padx=(0, 5))

    ctk.CTkLabel(toast, text=message, text_color="white",
                 justify="center", wraplength=1000, font=("Arial", 13)
                 ).pack(padx=15, pady=(0, 10))

    try:
        toast.attributes("-alpha", 0.0)
        for i in range(0, 11):
            toast.after(i * 30, lambda a=i: toast.attributes("-alpha", a / 10))
    except Exception:
        pass

    toast.after(3000, lambda: toast.destroy() if not is_pinned.get() else None)


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