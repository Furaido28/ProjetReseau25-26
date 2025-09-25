import customtkinter as ctk
from tkinter import messagebox
from models.SecurityManager import SecurityManager

security = SecurityManager("bdd/projetReseau.db")

def clear_root(root):
    for widget in root.winfo_children():
        widget.destroy()

def page_creer_mdp(root):
    def save_password():
        pwd = entry_password.get()
        if not pwd.strip():
            messagebox.showerror("Erreur", "Mot de passe vide interdit")
            return
        security.set_password(pwd)
        messagebox.showinfo("Succès", "Mot de passe enregistré !")
        clear_root(root)
        page_connexion(root)

    frame = ctk.CTkFrame(root, corner_radius=15, width=320, height=200)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Créer un mot de passe", font=("Arial", 18, "bold")).pack(pady=15)
    entry_password = ctk.CTkEntry(frame, placeholder_text="Nouveau mot de passe", show="*", width=250)
    entry_password.pack(pady=10)
    ctk.CTkButton(frame, text="Enregistrer", command=save_password).pack(pady=15)

def page_connexion(root):
    def login():
        user = entry_user.get()
        pwd = entry_password.get()
        if security.verify_password(pwd):
            messagebox.showinfo("Succès", f"Bienvenue {user} !")
            clear_root(root)
            page_menu(root)
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")

    frame = ctk.CTkFrame(root, corner_radius=15, width=320, height=260)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Connectez-vous", font=("Arial", 20, "bold")).pack(pady=(20, 10))
    entry_user = ctk.CTkEntry(frame, placeholder_text="Utilisateur", width=250)
    entry_user.pack(pady=10)
    entry_password = ctk.CTkEntry(frame, placeholder_text="Mot de passe", show="*", width=250)
    entry_password.pack(pady=10)
    ctk.CTkButton(frame, text="Connexion", width=200, command=login).pack(pady=20)

def page_menu(root):
    frame = ctk.CTkFrame(root, corner_radius=15, width=400, height=300)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Menu principal", font=("Arial", 20, "bold")).pack(pady=20)
    ctk.CTkButton(frame, text="Calcul adresse réseau", command=lambda: messagebox.showinfo("TODO", "À implémenter")).pack(pady=10)
    ctk.CTkButton(frame, text="Découpe en sous-réseaux", command=lambda: messagebox.showinfo("TODO", "À implémenter")).pack(pady=10)
