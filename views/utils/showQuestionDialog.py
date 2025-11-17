import customtkinter as ctk

def show_question_dialog(
    title: str,
    message: str,
    button1_text: str = "Oui",
    button2_text: str = "Non"
) -> bool:
    """
    Ouvre une boîte de dialogue CTk avec un message et deux boutons.

    Retourne:
        True  si button1 est cliqué
        False si button2 est cliqué ou si la fenêtre est fermée
    """
    PRIMARY = "#34A853"
    PRIMARY_HOVER = "#2C8E47"
    NEUTRAL = "#7F8C8D"

    result = {"value": False}

    # Fenêtre modale CTk
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.resizable(False, False)
    dialog.grab_set()
    dialog.focus_force()

    WIDTH = 480
    HEIGHT = 220
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

    # Header (titre + message)
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

    # Footer (boutons)
    footer = ctk.CTkFrame(container, corner_radius=12, fg_color="transparent")
    footer.pack(fill="x", padx=16, pady=(16, 16))
    footer.grid_columnconfigure(0, weight=1)
    footer.grid_columnconfigure(1, weight=1)

    def on_button1():
        result["value"] = True
        dialog.destroy()

    def on_button2():
        result["value"] = False
        dialog.destroy()

    btn1 = ctk.CTkButton(
        footer,
        text=button1_text,
        command=on_button1,
        height=44,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    )
    btn1.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    btn2 = ctk.CTkButton(
        footer,
        text=button2_text,
        command=on_button2,
        height=44,
        corner_radius=10,
        fg_color=NEUTRAL,
        hover_color=NEUTRAL,
        font=("Segoe UI Semibold", 18, "bold"),
    )
    btn2.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    # Bind clavier : Entrée = bouton1, Echap = bouton2
    dialog.bind("<Return>", lambda e: on_button1())
    dialog.bind("<KP_Enter>", lambda e: on_button1())
    dialog.bind("<Escape>", lambda e: on_button2())

    # Si on ferme par la croix → bouton2
    dialog.protocol("WM_DELETE_WINDOW", on_button2)

    # Attendre la fermeture (modal)
    dialog.wait_window()

    return result["value"]