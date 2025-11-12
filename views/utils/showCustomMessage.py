import customtkinter as ctk

def show_custom_message(title, message, type_="info", parent=None):
    # Palette d'accents harmonisée
    accent_colors = {
        "info": "#60A5FA",     # bleu doux
        "success": "#34A853",  # vert principal
        "warning": "#FACC15",  # jaune doux
        "error": "#ff4a4c",    # rouge pastel
    }
    accent_color = accent_colors.get(type_, "#60A5FA")

    # Arrière-plan et texte adoucis (dark mode équilibré)
    background_color = "#dbdbdb"
    bg_card = "#bababa"
    header_bg = "#878787"
    txt_main = "#151515"
    txt_sub = "#151515"

    # --- Conteneur principal ---
    toast = ctk.CTkFrame(
        parent,
        fg_color=bg_card,
        corner_radius=16,
        border_width=3,
        border_color=accent_color,
        bg_color=background_color,
    )
    toast.place(relx=0.5, rely=0.88, anchor="s")

    WIDTH = 700
    toast.configure(width=WIDTH)

    pinned = ctk.BooleanVar(value=False)

    def close_toast():
        toast.destroy()

    def toggle_pin():
        pinned.set(not pinned.get())
        pin_button.configure(text="📌" if pinned.get() else "📍")
        if not pinned.get():
            toast.after(7000, lambda: toast.destroy() if not pinned.get() else None)

    # --- Barre du haut ---
    header = ctk.CTkFrame(
        toast,
        fg_color=header_bg,
        corner_radius=16,
    )
    header.pack(fill="x", padx=12, pady=12)

    # --- Boule colorée à gauche ---
    color_dot = ctk.CTkFrame(
        header,
        fg_color=accent_color,
        corner_radius=50,
        width=18,
        height=18,
    )
    color_dot.pack(side="left", padx=(12, 10), pady=10)

    # --- Titre ---
    title_label = ctk.CTkLabel(
        header,
        text=title,
        font=("Segoe UI Semibold", 18, "bold"),
        text_color=txt_main,
        anchor="w",
        justify="left",
    )
    title_label.pack(side="left", padx=(0, 10))

    # --- Boutons à droite ---
    header_right = ctk.CTkFrame(header, fg_color="transparent")
    header_right.pack(side="right", padx=10)

    pin_button = ctk.CTkButton(
        header_right,
        text="📍",
        width=30,
        height=30,
        corner_radius=6,
        fg_color="transparent",
        hover_color="#3F3F3F",
        text_color=txt_main,
        command=toggle_pin,
        font=("Segoe UI", 16),
    )
    pin_button.pack(side="left", padx=(0, 8))

    close_button = ctk.CTkButton(
        header_right,
        text="✖",
        width=30,
        height=30,
        corner_radius=6,
        fg_color="transparent",
        hover_color="#7F1D1D",
        text_color=txt_main,
        command=close_toast,
        font=("Segoe UI", 16),
    )
    close_button.pack(side="left")

    # --- Corps du message ---
    body = ctk.CTkFrame(toast, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=24, pady=(0, 18))

    msg_label = ctk.CTkLabel(
        body,
        text=message,
        font=("Consolas", 16),
        text_color=txt_sub,
        anchor="w",
        justify="left",
        wraplength=WIDTH - 50,
    )
    msg_label.pack(fill="x")

    # --- Fermeture automatique ---
    toast.after(7000, lambda: toast.destroy() if not pinned.get() else None)
