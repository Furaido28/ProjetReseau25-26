import customtkinter as ctk
from views.utils.clearRoot import clear_root

def page_credits(root):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    clear_root(root)
    root.geometry("1200x700")

    PRIMARY = "#2ECC71"
    PRIMARY_HOVER = "#27AE60"

    # Layout global
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(root, corner_radius=16)
    container.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)

    container.grid_rowconfigure(0, weight=0)  # header
    container.grid_rowconfigure(1, weight=1)  # content
    container.grid_rowconfigure(2, weight=0)  # footer
    container.grid_columnconfigure(0, weight=1)

    # --- HEADER ---
    header = ctk.CTkFrame(container, corner_radius=16)
    header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text="Crédits du projet",
        font=("Segoe UI", 25, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(6, 0))

    ctk.CTkLabel(
        header,
        text="Travail réalisé dans le cadre du cours de réseaux (UE312)."
             "\nCet outil regroupe plusieurs fonctionnalités d'adressage IP et de découpe de sous-réseaux.",
        font=("Segoe UI", 18),
        justify="left",
        wraplength=1100,
    ).grid(row=1, column=0, sticky="w", pady=(0, 6))

    # --- CONTENU ---
    content_card = ctk.CTkFrame(container, corner_radius=16)
    content_card.grid(row=1, column=0, sticky="nsew", padx=16, pady=(8, 8))

    content_card.grid_columnconfigure(0, weight=1)

    # bloc infos
    info_text = (
        "Auteur / Développeur :\n"
        "    • Flipo Ethan\n"
        "    • Maréchal Leven\n"
        "    • Vanbercy Sailor\n\n"
        "Fonctionnalités principales :\n"
        "    • Calcul d'adresse réseau\n"
        "    • Vérification d'appartenance IP / masque\n"
        "    • Découpe de réseau en sous-réseaux (par nb d'IPs ou nb de SR)\n"
        "    • Vérification VLSM\n"
        "    • Sauvegarde et recherche des découpes dans une base de données\n\n"
        "Technologies utilisées :\n"
        "    • Python + CustomTkinter (interface graphique)\n"
        "    • ipaddress / netaddr (manipulation IP)\n"
        "    • Stockage des découpes en base de données\n"
    )

    ctk.CTkLabel(
        content_card,
        text=info_text,
        font=("Segoe UI", 18),
        justify="left",
        anchor="nw",
    ).grid(row=0, column=0, sticky="nw", padx=20, pady=20)

    # --- FOOTER ---
    footer = ctk.CTkFrame(container, corner_radius=12)
    footer.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
    footer.grid_columnconfigure(0, weight=1)

    # bouton retour menu
    def go_back():
        from .page_menu import page_menu
        page_menu(root)

    ctk.CTkButton(
        footer,
        text="Retour au menu",
        command=go_back,
        height=50,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    ).grid(row=0, column=0, pady=12, padx=6, sticky="ew")
