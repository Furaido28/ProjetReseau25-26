import customtkinter as ctk
# from tkinter import messagebox   # <-- à supprimer
from PIL import Image

from views.pages.page_menu import page_menu
from repository.SecurityManager import SecurityManager
from views.utils.tools import clear_root, show_custom_message
# si ta fonction est dans un autre module, importe-la :
# from views.utils.toasts import show_custom_message
# sinon, colle directement ta définition de show_custom_message dans ce fichier.

security = SecurityManager("bdd/projetReseau.db")

def page_connexion(root):
    clear_root(root)

    # --- Fenêtre compacte et centrée ---
    root.geometry("500x380")

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    # --- Titre ---
    ctk.CTkLabel(
        frame,
        text="Connectez-vous",
        font=("Arial", 22, "bold"),
        text_color="black"
    ).pack(pady=(10, 25))

    # --- Champ utilisateur ---
    entry_user = ctk.CTkEntry(
        frame,
        placeholder_text="Nom d'utilisateur",
        height=40,
        font=("Arial", 14),
        corner_radius=10
    )
    entry_user.pack(pady=10, padx=40, fill="x")

    # --- Champ mot de passe ---
    entry_password = ctk.CTkEntry(
        frame,
        placeholder_text="Mot de passe",
        show="*",
        height=40,
        font=("Arial", 14),
        corner_radius=10
    )
    entry_password.pack(pady=10, padx=40, fill="x")

    # --- Fonction de connexion ---
    def login():
        username = entry_user.get().strip()
        pwd = entry_password.get()

        if security.verify_password(pwd):
            root.current_user = username or "invité"

            # On charge le menu AVANT d'afficher le toast pour qu'il survive au clear_root
            clear_root(root)
            page_menu(root)
        else:
            # Toast erreur (pas de clear_root ici)
            show_custom_message(
                title="Erreur",
                message="Mot de passe incorrect.",
                type_="error",
                parent=root
            )

    # --- Icône Connexion (réduite) ---
    icon_login = ctk.CTkImage(dark_image=Image.open("assets/icons/login.png"), size=(24, 24))

    # --- Bouton Connexion (style élégant, sans cadre) ---
    btn_login = ctk.CTkButton(
        frame,
        text="Se connecter",
        image=icon_login,
        command=login,
        corner_radius=25,
        width=220,
        height=48,
        fg_color="#2ECC71",
        hover_color="#27AE60",
        text_color="white",
        font=("Segoe UI Semibold", 17, "bold"),
        compound="left",
        border_width=0
    )
    btn_login.pack(pady=25, padx=20)

    # --- Touche Entrée = Connexion ---
    root.bind("<Return>", lambda event: login())