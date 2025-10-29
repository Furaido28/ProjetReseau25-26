import customtkinter as ctk

from controllers.NetworkService import NetworkService
from views.pages.page_menu import page_menu
from views.utils.clearRoot import clear_root
from views.utils.showCustomMessage import show_custom_message
from views.utils.showInputDialog import show_input_dialog

network_service = NetworkService()

def page_verif_adresse_reseau(root):
    # ---------------------------
    # THÈME / FENÊTRE
    # ---------------------------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    clear_root(root)
    root.geometry("1250x625")

    # ---------------------------
    # COULEURS / STYLE
    # ---------------------------
    PRIMARY = "#34A853"
    PRIMARY_HOVER = "#2C8E47"

    # ---------------------------
    # LOGIQUE
    # ---------------------------
    def verifier():
        ip = entry_ip.get().strip()
        network_ip = entry_network_ip.get().strip()
        network_mask = entry_network_mask.get().strip()

        # vérif des champs requis
        if not ip or not network_ip or not network_mask:
            show_custom_message(
                "Erreur",
                "Tous les champs sont obligatoires.",
                "error"
            )
            return

        # format du masque
        if not network_mask.startswith("/"):
            show_custom_message(
                "Erreur",
                "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0",
                "error"
            )
            return

        mask_clean = network_mask[1:].strip()

        try:
            # define_ip_in_network retourne:
            #  (isInNetwork: bool, firstHost, lastHost, errorMsg)
            result, first, last, error = network_service.define_ip_in_network(
                ip,
                network_ip,
                mask_clean
            )

            if error:
                # erreur côté service/réseau -> toast rouge
                show_custom_message(
                    "Erreur",
                    f"Erreur : {error}",
                    "error"
                )
                return

            if result:
                # ✅ l'IP appartient
                msg = (
                    f"✅ L'adresse IP {ip} appartient au réseau "
                    f"{network_ip}/{mask_clean}\n\n"
                    f"Première IP utilisable de la plage : {first}\n"
                    f"Dernière IP utilisable de la plage : {last}"
                )
                show_custom_message(
                    "Adresse dans le réseau",
                    msg,
                    "success"
                )
            else:
                # ❌ l'IP n'appartient pas
                msg = (
                    f"❌ L'adresse IP {ip} n'appartient PAS au réseau "
                    f"{network_ip}/{mask_clean}"
                )
                show_custom_message(
                    "Adresse hors réseau",
                    msg,
                    "error"
                )

        except Exception as e:
            # exception inattendue -> toast rouge
            show_custom_message(
                "Erreur",
                f"Exception : {e}",
                "error"
            )

    # ---------------------------
    # LAYOUT PRINCIPAL
    # ---------------------------
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(root, corner_radius=16)
    container.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)

    # même structure que page_adresse_reseau:
    # 0 = header, 1 = form, 2 = actions, 3 = filler/espace
    container.grid_rowconfigure(0, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(2, weight=0)
    container.grid_rowconfigure(3, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # ---------------------------
    # En-tête
    # ---------------------------
    header = ctk.CTkFrame(container, corner_radius=16)
    header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text="Vérification d'appartenance d'une IP à un réseau",
        font=("Segoe UI", 25, "bold"),
    ).grid(row=0, column=0, sticky="w", pady=(6, 0))

    ctk.CTkLabel(
        header,
        text=(
            "Cette page vérifie si une IP donnée appartient à un réseau (IP réseau + masque)"
            " et affiche la plage d'adresses utilisables si elle est dedans."
        ),
        font=("Segoe UI", 20),
        wraplength=1150,
        justify="left",
    ).grid(row=1, column=0, sticky="w", pady=(0, 6))

    # ---------------------------
    # Formulaire
    # ---------------------------
    form_card = ctk.CTkFrame(container, corner_radius=16)
    form_card.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 8))
    form_card.grid_columnconfigure(0, weight=0)
    form_card.grid_columnconfigure(1, weight=1)

    # Ligne 1 : IP testée
    ctk.CTkLabel(form_card, text="IP à tester", font=("Segoe UI", 15)).grid(
        row=0,
        column=0,
        sticky="e",
        padx=(16, 10),
        pady=(16, 8)
    )
    entry_ip = ctk.CTkEntry(
        form_card,
        placeholder_text="ex : 192.168.1.42",
        height=36
    )
    entry_ip.grid(
        row=0,
        column=1,
        sticky="ew",
        padx=(0, 16),
        pady=(16, 8)
    )

    # Ligne 2 : IP réseau
    ctk.CTkLabel(form_card, text="IP réseau", font=("Segoe UI", 15)).grid(
        row=1,
        column=0,
        sticky="e",
        padx=(16, 10),
        pady=8
    )
    entry_network_ip = ctk.CTkEntry(
        form_card,
        placeholder_text="ex : 192.168.1.0",
        height=36
    )
    entry_network_ip.grid(
        row=1,
        column=1,
        sticky="ew",
        padx=(0, 16),
        pady=8
    )

    # Ligne 3 : Masque
    ctk.CTkLabel(form_card, text="Masque", font=("Segoe UI", 15)).grid(
        row=2,
        column=0,
        sticky="e",
        padx=(16, 10),
        pady=8
    )
    entry_network_mask = ctk.CTkEntry(
        form_card,
        placeholder_text="ex : /24 ou /255.255.255.0",
        height=36
    )
    entry_network_mask.grid(
        row=2,
        column=1,
        sticky="ew",
        padx=(0, 16),
        pady=8
    )

    # ---------------------------
    # Boutons d'action
    # ---------------------------
    actions = ctk.CTkFrame(container, corner_radius=12)
    actions.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
    actions.grid_columnconfigure(0, weight=1)
    actions.grid_columnconfigure(1, weight=1)

    ctk.CTkButton(
        actions,
        text="Vérifier",
        command=verifier,
        height=44,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    ).grid(
        row=0,
        column=0,
        sticky="ew",
        padx=6,
        pady=8
    )

    ctk.CTkButton(
        actions,
        text="Retour menu",
        command=lambda: page_menu(root),
        height=44,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    ).grid(
        row=0,
        column=1,
        sticky="ew",
        padx=6,
        pady=8
    )

    # ---------------------------
    # Plus de zone résultat fixe en bas,
    # la row=3 du container reste juste pour donner de l'air visuel
    # ---------------------------
    filler = ctk.CTkFrame(container, corner_radius=16)
    filler.grid(row=3, column=0, sticky="nsew", padx=16, pady=(8, 16))
    filler.grid_rowconfigure(0, weight=1)
    filler.grid_columnconfigure(0, weight=1)