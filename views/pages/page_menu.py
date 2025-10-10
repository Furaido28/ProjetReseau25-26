import customtkinter as ctk

from views.utils.tools import clear_root

def page_menu(root):
    clear_root(root)
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    username = getattr(root, "current_user", None) or "invité"

    ctk.CTkLabel(frame, text=f"Menu principal, bienvenue {username}", font=("Arial", 22, "bold")).pack(pady=20)

    def go_page_calcul_adresse_res():
        from .page_calcul_adresse_res import page_adresse_reseau
        page_adresse_reseau(root)

    def go_page_verif_adresse_res():
        from .page_verif_adresse_res import page_verif_adresse_reseau
        page_verif_adresse_reseau(root)

    def go_page_decoupe_adresse_res():
        from .page_decoupe_adresse_res import page_decoupe_mode
        page_decoupe_mode(root)

    def go_page_verif_decoupe_vlsmm():
        from .page_verif_decoupe_vlsm import page_verif_decoupe_vlsm
        page_verif_decoupe_vlsm(root)

    ctk.CTkButton(frame, text="Calcul adresse réseau",
                  command=go_page_calcul_adresse_res).pack(fill="x", padx=60, pady=10)
    ctk.CTkButton(frame, text="Vérification d'une adresse IP",
                  command=go_page_verif_adresse_res).pack(fill="x", padx=60, pady=10)
    ctk.CTkButton(frame, text="Découpe par nb SR ou nb IP",
                  command=go_page_decoupe_adresse_res).pack(fill="x", padx=60, pady=10)
    ctk.CTkButton(frame, text="Vérification d'une découpe VLSM",
                  command=go_page_verif_decoupe_vlsmm).pack(fill="x", padx=60, pady=10)