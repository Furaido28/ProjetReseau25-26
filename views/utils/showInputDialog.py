import customtkinter as ctk

def show_input_dialog(title: str, message: str) -> str | None:
    PRIMARY = "#34A853"
    PRIMARY_HOVER = "#2C8E47"

    result = {"value": None}

    # Fenêtre modale CTk
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.resizable(False, False)
    dialog.grab_set()
    dialog.focus_force()

    # dimensions "carte" cohérentes
    WIDTH = 480
    HEIGHT = 275
    dialog.geometry(f"{WIDTH}x{HEIGHT}")

    # Centrer la fenêtre à l'écran
    dialog.update_idletasks()
    screen_w = dialog.winfo_screenwidth()
    screen_h = dialog.winfo_screenheight()
    pos_x = int(screen_w / 2 - WIDTH / 2)
    pos_y = int(screen_h / 3 - HEIGHT / 2)
    dialog.geometry(f"{WIDTH}x{HEIGHT}+{pos_x}+{pos_y}")

    # Conteneur principal (carte arrondie)
    container = ctk.CTkFrame(dialog, corner_radius=16)
    container.pack(expand=True, fill="both", padx=20, pady=20)

    # Header (titre + message d'instructions)
    header = ctk.CTkFrame(container, corner_radius=16, fg_color="transparent")
    header.pack(fill="x", padx=16, pady=(16, 8))

    ctk.CTkLabel(
        header,
        text=title,
        font=("Segoe UI", 22, "bold"),
        anchor="w",
        justify="left",
    ).pack(anchor="w")

    ctk.CTkLabel(
        header,
        text=message,
        font=("Segoe UI", 16),
        wraplength=440,
        justify="left",
        anchor="w",
        text_color="#4B5563",
    ).pack(anchor="w", pady=(6, 0))

    # Zone de saisie
    form = ctk.CTkFrame(container, corner_radius=12, fg_color="transparent")
    form.pack(fill="x", padx=16, pady=(8, 8))

    entry = ctk.CTkEntry(
        form,
        height=40,
        placeholder_text="Entrez une valeur ici...",
        font=("Segoe UI", 15),
    )
    entry.pack(fill="x")
    entry.focus_set()

    # Actions (boutons OK / Annuler)
    footer = ctk.CTkFrame(container, corner_radius=12, fg_color="transparent")
    footer.pack(fill="x", padx=16, pady=(16, 16))
    footer.grid_columnconfigure(0, weight=1)
    footer.grid_columnconfigure(1, weight=1)

    def confirm_and_close():
        result["value"] = entry.get().strip()
        dialog.destroy()

    def cancel_and_close():
        result["value"] = None
        dialog.destroy()

    btn_ok = ctk.CTkButton(
        footer,
        text="Valider",
        command=confirm_and_close,
        height=44,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    )
    btn_ok.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    btn_cancel = ctk.CTkButton(
        footer,
        text="Annuler",
        command=cancel_and_close,
        height=44,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    )
    btn_cancel.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    # Bind clavier : Entrée = OK, Echap = Annuler
    dialog.bind("<Return>", lambda e: confirm_and_close())
    dialog.bind("<KP_Enter>", lambda e: confirm_and_close())
    dialog.bind("<Escape>", lambda e: cancel_and_close())

    # Empêche la fermeture par la croix sans gérer le return
    dialog.protocol("WM_DELETE_WINDOW", cancel_and_close)

    # Attendre la fermeture (modal)
    dialog.wait_window()

    return result["value"]