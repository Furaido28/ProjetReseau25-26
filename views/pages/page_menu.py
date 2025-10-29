import customtkinter as ctk
from PIL import Image
from views.utils.clearRoot import clear_root
from views.utils.showCustomMessage import show_custom_message
from views.utils.showInputDialog import show_input_dialog

def page_menu(root):
    # Thème global (identique aux autres pages)
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    clear_root(root)
    root.geometry("1200x700")

    # ---------------------------
    # COULEURS / STYLE
    # ---------------------------
    PRIMARY = "#2ECC71"
    PRIMARY_HOVER = "#27AE60"
    DISABLED = "#7F8C8D"
    DANGER = "#34A853"
    DANGER_HOVER = "#2C8E47"

    username = getattr(root, "current_user", None) or "invité"

    # ---------------------------
    # NAVIGATION
    # ---------------------------
    def go_page_calcul_adresse_res():
        from .page_calcul_adresse_res import page_adresse_reseau
        page_adresse_reseau(root)

    def go_page_verif_adresse_res():
        from .page_verif_adresse_res import page_verif_adresse_reseau
        page_verif_adresse_reseau(root)

    def go_page_decoupe_adresse_res():
        from .page_decoupe_adresse_res import page_decoupe_mode
        page_decoupe_mode(root)

    def go_page_verif_decoupe_vlsmm():
        from .page_verif_decoupe_vlsm import page_verif_decoupe_vlsm
        page_verif_decoupe_vlsm(root)

    def go_page_recherche_decoupe():
        from .page_recherche_decoupe import page_recherche_decoupe
        page_recherche_decoupe(root)

    def go_page_credits():
        from .page_credits import page_credits
        page_credits(root)

    # ---------------------------
    # LAYOUT PRINCIPAL
    # ---------------------------
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(root, corner_radius=16)
    container.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
    container.grid_rowconfigure(0, weight=0)  # header
    container.grid_rowconfigure(1, weight=1)  # content
    container.grid_rowconfigure(2, weight=0)  # footer
    container.grid_columnconfigure(0, weight=1)

    # ---------------------------
    # HEADER
    # ---------------------------
    header = ctk.CTkFrame(container, corner_radius=16)
    header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text=f"Menu principal",
        font=("Segoe UI", 25, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(6, 0))

    ctk.CTkLabel(
        header,
        text="Choisissez un outil réseau ci-dessous.",
        font=("Segoe UI", 20),
        wraplength=1000,
        justify="left"
    ).grid(row=1, column=0, sticky="w", pady=(0, 6))

    # ---------------------------
    # CONTENU : Carte avec les boutons
    # ---------------------------
    content_card = ctk.CTkFrame(container, corner_radius=16)
    content_card.grid(row=1, column=0, sticky="nsew", padx=16, pady=(8, 8))

    for i in range(2):
        content_card.grid_columnconfigure(i, weight=1, uniform="col")
    for r in range(3):
        content_card.grid_rowconfigure(r, weight=1, uniform="row")

    # icônes
    def load_icon(path):
        try:
            return ctk.CTkImage(dark_image=Image.open(path), size=(36, 36))
        except Exception:
            return None

    img_calc = load_icon("assets/icons/calc.png")
    img_verif = load_icon("assets/icons/verif.png")
    img_decoupe = load_icon("assets/icons/decoupe.png")
    img_vlsm = load_icon("assets/icons/vlsm.png")
    img_recherche = load_icon("assets/icons/recherche.png")

    btn_style = {
        "height": 90,
        "width": 170,
        "corner_radius": 8,
        "fg_color": "#D5F5E3",      # vert très clair
        "hover_color": "#ABEBC6",   # hover
        "text_color": "#145A32",    # vert foncé
        "font": ("Segoe UI", 20, "bold"),
        "compound": "top"
    }

    ctk.CTkButton(
        content_card,
        text="Recherche découpe",
        image=img_recherche,
        compound="left",
        command=go_page_recherche_decoupe,
        height=90,
        corner_radius=8,
        fg_color="#D5F5E3",
        hover_color="#ABEBC6",
        text_color="#145A32",
        font=("Segoe UI", 20, "bold")
    ).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

    ctk.CTkButton(
        content_card,
        text="Calcul\nadresse réseau",
        image=img_calc,
        command=go_page_calcul_adresse_res,
        **btn_style,
    ).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    ctk.CTkButton(
        content_card,
        text="Vérification\nadresse IP",
        image=img_verif,
        command=go_page_verif_adresse_res,
        **btn_style
    ).grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    ctk.CTkButton(
        content_card,
        text="Découpe\npar nb SR ou IP",
        image=img_decoupe,
        command=go_page_decoupe_adresse_res,
        **btn_style
    ).grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    ctk.CTkButton(
        content_card,
        text="Vérification\ndécoupe VLSM",
        image=img_vlsm,
        command=go_page_verif_decoupe_vlsmm,
        **btn_style
    ).grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    # ---------------------------
    # FOOTER
    # ---------------------------
    footer = ctk.CTkFrame(container, corner_radius=12)
    footer.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))

    # 2 colonnes pour aligner les deux boutons côte à côte
    footer.grid_columnconfigure(0, weight=1)
    footer.grid_columnconfigure(1, weight=1)

    # Bouton Crédits
    ctk.CTkButton(
        footer,
        text="Crédits",
        command=go_page_credits,
        height=50,
        width=200,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    ).grid(row=0, column=0, pady=12, padx=6, sticky="ew")

    # Bouton Déconnexion
    ctk.CTkButton(
        footer,
        text=f"Déconnexion ({username})",
        command=root.destroy,
        height=50,
        width=200,
        corner_radius=10,
        fg_color="#E74C3C",         # rouge logout
        hover_color="#C0392B",
        font=("Segoe UI Semibold", 18, "bold"),
    ).grid(row=0, column=1, pady=12, padx=6, sticky="ew")
