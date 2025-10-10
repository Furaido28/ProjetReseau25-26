import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from views.utils.tools import clear_root
from repository.SecurityManager import SecurityManager
from .page_connexion import page_connexion

security = SecurityManager("bdd/projetReseau.db")

def page_creer_mdp(root):
    clear_root(root)
    ctk.set_appearance_mode("dark")

    GREEN_BG = "#D5F5E3"
    GREEN_HOVER = "#ABEBC6"
    GREEN_DARK = "#145A32"

    # --- Fenêtre centrée et compacte ---
    root.geometry("500x350")
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    # --- Titre ---
    ctk.CTkLabel(
        frame,
        text="Créer un mot de passe",
        font=("Arial", 22, "bold"),
        text_color="white"
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

    # --- Bouton Enregistrer (logo au-dessus) ---
    icon_save = ctk.CTkImage(dark_image=Image.open("assets/icons/save.png"), size=(40, 40))

    def save_password():
        pwd = entry_password.get()
        if not pwd.strip():
            messagebox.showerror("Erreur", "Mot de passe vide interdit.")
            return
        security.set_password(pwd)
        messagebox.showinfo("Succès", "Mot de passe enregistré !")
        clear_root(root)
        page_connexion(root)

    ctk.CTkButton(
        frame,
        text="Enregistrer",
        image=icon_save,
        command=save_password,
        corner_radius=5,
        width=160,
        height=120,
        fg_color=GREEN_BG,
        hover_color=GREEN_HOVER,
        text_color=GREEN_DARK,
        font=("Arial", 14, "bold"),
        compound="top"
    ).pack(pady=25)

    # --- Bouton Retour ---
    ctk.CTkButton(
        frame,
        text="Retour",
        command=lambda: page_connexion(root),
        fg_color="#E74C3C",
        hover_color="#C0392B",
        corner_radius=8,
        width=100,
        height=35,
        font=("Arial", 13, "bold")
    ).pack(pady=(10, 0))
