import customtkinter as ctk
from models import AppGui
from models.AppGui import page_menu
from models.SecurityManager import SecurityManager
#test
security = SecurityManager("bdd/projetReseau.db")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Projet Réseau")
root.geometry("900x700")
root.resizable(True, True)

if security.has_password():
    AppGui.page_connexion(root)
else:
    AppGui.page_creer_mdp(root)

root.mainloop()

security.close()
