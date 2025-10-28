import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from views.utils.tools import clear_root
from repository.SecurityManager import SecurityManager
from .page_connexion import page_connexion

security = SecurityManager("bdd/projetReseau.db")

def page_creer_mdp(root):
    clear_root(root)

    # --- Fenêtre centrée et compacte ---
    root.geometry("500x300")
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

    # --- Icône Enregistrer (réduite) ---
    icon_save = ctk.CTkImage(dark_image=Image.open("assets/icons/login.png"), size=(24, 24))

    def save_password():
        pwd = entry_password.get()
        if not pwd.strip():
            messagebox.showerror("Erreur", "Mot de passe vide interdit.")
            return
        security.set_password(pwd)
        messagebox.showinfo("Succès", "Mot de passe enregistré !")
        clear_root(root)
        page_connexion(root)

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
