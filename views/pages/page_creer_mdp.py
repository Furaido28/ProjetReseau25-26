import customtkinter as ctk
from tkinter import messagebox
from views.utils.tools import clear_root
from repository.SecurityManager import SecurityManager
from .page_connexion import page_connexion

security = SecurityManager("bdd/projetReseau.db")

def page_creer_mdp(root):
    clear_root(root)

    def save_password():
        pwd = entry_password.get()
        if not pwd.strip():
            messagebox.showerror("Erreur", "Mot de passe vide interdit.")
            return
        security.set_password(pwd)
        messagebox.showinfo("Succès", "Mot de passe enregistré !")
        clear_root(root)
        page_connexion(root)

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Créer un mot de passe", font=("Arial", 22, "bold")).pack(pady=(10, 15))
    entry_password = ctk.CTkEntry(frame, placeholder_text="Nouveau mot de passe", show="*", height=30)
    entry_password.pack(pady=10, padx=40, fill="x")

    ctk.CTkButton(frame, text="Enregistrer", command=save_password,
                  height=40, corner_radius=10).pack(pady=15, padx=40, fill="x")