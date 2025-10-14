import customtkinter as ctk
from PIL import Image
from views.utils.tools import clear_root

def page_menu(root):
    clear_root(root)
    root.geometry("900x700")

    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    username = getattr(root, "current_user", None) or "invité"

    ctk.CTkLabel(
        frame,
        text=f"Menu principal — Bienvenue {username}",
        font=("Arial", 22, "bold")
    ).pack(pady=30)

    # --- Chargement des icônes ---
    img_calc = ctk.CTkImage(dark_image=Image.open("assets/icons/calc.png"), size=(40, 40))
    img_verif = ctk.CTkImage(dark_image=Image.open("assets/icons/verif.png"), size=(40, 40))
    img_decoupe = ctk.CTkImage(dark_image=Image.open("assets/icons/decoupe.png"), size=(40, 40))
    img_vlsm = ctk.CTkImage(dark_image=Image.open("assets/icons/vlsm.png"), size=(40, 40))

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

    # --- Cadre pour les boutons ---
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(pady=20)

    # --- Style commun des boutons ---
    btn_style = {
        "corner_radius": 5,          # Carré
        "width": 150,
        "height": 120,
        "fg_color": "#D5F5E3",       # Fond vert clair
        "hover_color": "#ABEBC6",    # Survol
        "text_color": "#145A32",     # Vert foncé
        "font": ("Arial", 14, "bold"),
        "compound": "top"            # Image au-dessus du texte
    }

    # --- Boutons avec logo au-dessus ---
    ctk.CTkButton(
        btn_frame, text="Calcul\nadresse réseau",
        image=img_calc, command=go_page_calcul_adresse_res, **btn_style
    ).grid(row=0, column=0, padx=20, pady=20)

    ctk.CTkButton(
        btn_frame, text="Vérification\nadresse IP",
        image=img_verif, command=go_page_verif_adresse_res, **btn_style
    ).grid(row=0, column=1, padx=20, pady=20)

    ctk.CTkButton(
        btn_frame, text="Découpe\npar nb SR ou IP",
        image=img_decoupe, command=go_page_decoupe_adresse_res, **btn_style
    ).grid(row=1, column=0, padx=20, pady=20)

    ctk.CTkButton(
        btn_frame, text="Vérification\ndécoupe VLSM",
        image=img_vlsm, command=go_page_verif_decoupe_vlsmm, **btn_style
    ).grid(row=1, column=1, padx=20, pady=20)

    # --- Bouton Quitter ---
    ctk.CTkButton(
        frame, text="Quitter", command=root.destroy,
        fg_color="#E74C3C", hover_color="#C0392B",
        corner_radius=10, font=("Arial", 14, "bold")
    ).pack(pady=20)
