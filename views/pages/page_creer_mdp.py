import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from views.utils.clearRoot import clear_root
from views.utils.showCustomMessage import show_custom_message
from views.utils.showInputDialog import show_input_dialog

from repository.SecurityManager import SecurityManager
from .page_connexion import page_connexion

security = SecurityManager("bdd/projetReseau.db")

def page_creer_mdp(root):
    clear_root(root)

    # --- Fenêtre centrée et compacte ---
    root.geometry("500x380")
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    # --- Titre ---
    ctk.CTkLabel(
        frame,
        text="Créer un mot de passe",
        font=("Arial", 22, "bold"),
        text_color="black"
    ).pack(pady=(10, 25))

    # --- Champ mot de passe ---
    entry_password = ctk.CTkEntry(
        frame,
        placeholder_text="Nouveau mot de passe",
        show="*",
        height=40,
        font=("Arial", 14),
        corner_radius=10
    )
    entry_password.pack(pady=10, padx=40, fill="x")
    # --- Champ de confirmation mot de passe ---
    confirmed_password = ctk.CTkEntry(
        frame,
        placeholder_text="Confirmer mot de passe",
        show="*",
        height=40,
        font=("Arial", 14),
        corner_radius=10
    )
    confirmed_password.pack(pady=10, padx=40, fill="x")

    # --- Icône Enregistrer (réduite) ---
    icon_save = ctk.CTkImage(dark_image=Image.open("assets/icons/login.png"), size=(24, 24))

    def save_password():
        if entry_password.get() == confirmed_password.get():
            pwd = entry_password.get()
            if not pwd.strip():
                show_custom_message("Erreur", "Mot de passe vide interdit.", "error")
                return
            security.set_password(pwd)
            clear_root(root)
            page_connexion(root)
        else :
            show_custom_message(
                "Erreur",
                f"Les 2 mots de passe ne correspondent pas",
                "error"
            )

    # --- Bouton Enregistrer (style élégant / moderne) ---
    btn_save = ctk.CTkButton(
        frame,
        text="Enregistrer",
        image=icon_save,
        command=save_password,
        corner_radius=25,
        width=220,
        height=48,
        fg_color="#34A853",  # vert moderne
        hover_color="#2C8E47",  # plus foncé au survol
        text_color="white",
        font=("Segoe UI Semibold", 17, "bold"),
        compound="left",  # icône à gauche du texte
        border_width=0  # pas de cadre
    )
    btn_save.pack(pady=25, padx=20)