import customtkinter as ctk
from repository.SecurityManager import SecurityManager

# importe uniquement les pages utiles au démarrage
from views.pages.page_connexion import page_connexion
from views.pages.page_creer_mdp import page_creer_mdp
from views.pages.page_verif_decoupe_vlsm import page_verif_decoupe_vlsm


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.title("Projet Réseau")
    root.resizable(True, True)

    security = SecurityManager("bdd/projetReseau.db")
    # (optionnel) rendre le service accessible partout via root
    root.security = security

    # Choix de la page d'accueil
    if security.has_password():
        page_connexion(root)
    else:
        page_creer_mdp(root)

    # Si tu veux démarrer directement sur une autre page S:
    # page_verif_decoupe_vlsm(root)

    root.mainloop()
    security.close()

if __name__ == "__main__":
    main()