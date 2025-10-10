import customtkinter as ctk
from tkinter import messagebox

from views.pages.page_menu import page_menu
from repository.SecurityManager import SecurityManager
from views.utils.tools import clear_root

security = SecurityManager("bdd/projetReseau.db")

def page_connexion(root):
    clear_root(root)

    def login():
        username = entry_user.get().strip()
        pwd = entry_password.get()
        if security.verify_password(pwd):
            root.current_user = username  # ou un dict/objet user complet
            messagebox.showinfo("Succès", f"Bienvenue {username} !")
            clear_root(root)
            page_menu(root)
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Connectez-vous", font=("Arial", 22, "bold")).pack(pady=(10, 20))
    entry_user = ctk.CTkEntry(frame, placeholder_text="Utilisateur", height=30)
    entry_user.pack(pady=8, padx=40, fill="x")

    entry_password = ctk.CTkEntry(frame, placeholder_text="Mot de passe", show="*", height=30)
    entry_password.pack(pady=8, padx=40, fill="x")

    ctk.CTkButton(frame, text="Connexion", command=login,
                  height=40, corner_radius=10).pack(pady=20, padx=40, fill="x")
    root.bind("<Return>", lambda event: login())