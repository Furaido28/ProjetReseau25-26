import customtkinter as ctk
from tkinter import messagebox

def clear_root(root):
    """Efface tout le contenu de la fenêtre."""
    for widget in root.winfo_children():
        widget.destroy()


def show_custom_message(title, message, type_="info", parent=None):
    """Affiche une notification toast élégante, large et épinglable."""
    colors = {
        "info": "#3B82F6",
        "success": "#22C55E",
        "warning": "#EAB308",
        "error": "#EF4444",
    }
    color = colors.get(type_, "#3B82F6")

    # --- Conteneur principal du toast ---
    toast = ctk.CTkFrame(parent, fg_color=color, corner_radius=20)
    toast.place(relx=0.5, rely=0.93, anchor="s")  # légèrement au-dessus du bas

    is_pinned = ctk.BooleanVar(value=False)

    def close_toast():
        toast.destroy()

    def toggle_pin():
        is_pinned.set(not is_pinned.get())
        if is_pinned.get():
            pin_button.configure(text="📌", fg_color="#1E3A8A")
        else:
            pin_button.configure(text="📍", fg_color=color)
            toast.after(4500, lambda: toast.destroy() if not is_pinned.get() else None)

    # --- En-tête ---
    header = ctk.CTkFrame(toast, fg_color="transparent")
    header.pack(fill="x", padx=15, pady=(10, 0))

    ctk.CTkLabel(
        header,
        text=title,
        font=("Segoe UI Semibold", 20, "bold"),  # plus grand
        text_color="white",
        anchor="w"
    ).pack(side="left", padx=(10, 0))

    pin_button = ctk.CTkButton(
        header,
        text="📍",
        width=36, height=32,
        corner_radius=10,
        fg_color=color,
        hover_color="#1E3A8A",
        text_color="white",
        font=("Arial", 15),
        command=toggle_pin
    )
    pin_button.pack(side="right", padx=(0, 6))

    close_button = ctk.CTkButton(
        header,
        text="✖",
        width=36, height=32,
        corner_radius=10,
        fg_color=color,
        hover_color="#991B1B",
        text_color="white",
        font=("Arial", 15, "bold"),
        command=close_toast
    )
    close_button.pack(side="right", padx=(0, 8))

    # --- Message principal ---
    ctk.CTkLabel(
        toast,
        text=message,
        text_color="white",
        justify="center",
        wraplength=850,  # <-- plus large pour le texte
        font=("Segoe UI", 17),  # légèrement plus grand
        anchor="center"
    ).pack(padx=30, pady=(5, 15))

    # --- Animation d’apparition ---
    try:
        toast.attributes("-alpha", 0.0)
        for i in range(0, 11):
            toast.after(i * 25, lambda a=i: toast.attributes("-alpha", a / 10))
    except Exception:
        pass

    # --- Fermeture automatique ---
    toast.after(4500, lambda: toast.destroy() if not is_pinned.get() else None)


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