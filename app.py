import customtkinter as ctk
from repository.SecurityManager import SecurityManager
from views.utils.paths import ensure_db_initialized, resource_path

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.title("Projet Réseau")
    try:
        root.iconbitmap(resource_path("assets/app.ico"))
    except Exception:
        pass

    # 1) Préparer la BDD utilisateur
    db_path = ensure_db_initialized()
    security = SecurityManager(str(db_path))
    root.security = security

    # 2) IMPORTS ICI (après init BDD) ✅
    from views.pages.page_connexion import page_connexion
    from views.pages.page_creer_mdp import page_creer_mdp

    # 3) Navigation
    if security.has_password():
        page_connexion(root)
    else:
        page_creer_mdp(root)

    root.mainloop()
    security.close()

if __name__ == "__main__":
    main()
