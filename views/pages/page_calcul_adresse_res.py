import customtkinter as ctk

from controllers.NetworkService import NetworkService
from views.pages.page_menu import page_menu
from views.utils.tools import clear_root, show_custom_message

network_service = NetworkService()


def page_adresse_reseau(root):
    # ---------------------------
    # THÈME / FENÊTRE
    # ---------------------------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    clear_root(root)
    root.geometry("1250x700")

    # ---------------------------
    # COULEURS / STYLE
    # ---------------------------
    PRIMARY = "#2ECC71"
    PRIMARY_HOVER = "#27AE60"
    DANGER = "#E74C3C"
    DANGER_HOVER = "#C0392B"

    # ---------------------------
    # LOGIQUE
    # ---------------------------
    def verifier() -> bool:
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        mode_label = var_mode.get()
        mode = "classless" if mode_label.lower().startswith("classless") else "classful"

        if not ip:
            show_custom_message("Erreur", "L'adresse IP est obligatoire.", "error")
            return False

        if mode == "classless":
            if not mask:
                show_custom_message("Erreur", "Le masque est obligatoire en mode classless.", "error")
                return False
            if not mask.startswith("/"):
                show_custom_message(
                    "Erreur",
                    "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0",
                    "error",
                )
                return False
        else:  # classful
            if mask and not mask.startswith("/"):
                show_custom_message(
                    "Erreur",
                    "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0",
                    "error",
                )
                return False
        return True

    def calculer():
        if not verifier():
            return

        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        mode_label = var_mode.get()
        mode = "classless" if mode_label.lower().startswith("classless") else "classful"

        try:
            mask_to_use = mask[1:] if mask else None
            is_classful = (mode == "classful")
            result = network_service.calculate(ip, mask_to_use, is_classful)

            text_result.configure(state="normal")
            text_result.delete("1.0", "end")
            text_result.insert("end", result)
            text_result.configure(state="disabled")
        except Exception as e:
            text_result.configure(state="normal")
            text_result.delete("1.0", "end")
            text_result.insert("end", f"Erreur : {e}")
            text_result.configure(state="disabled")

    # ---------------------------
    # LAYOUT PRINCIPAL
    # ---------------------------
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(root, corner_radius=16)
    container.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
    container.grid_rowconfigure(0, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(2, weight=0)
    container.grid_rowconfigure(3, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # En-tête
    header = ctk.CTkFrame(container, corner_radius=16)
    header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text="Calcul d’adresse réseau",
        font=("Segoe UI", 25, "bold"),
    ).grid(row=0, column=0, sticky="w", pady=(6, 0))

    ctk.CTkLabel(
        header,
        text="Cette page calcule les informations réseau (adresse, masque, broadcast, etc.) à partir d’une IP en mode Classless (CIDR) ou Classful.",
        font=("Segoe UI", 20),
        wraplength=1150,
        justify="left",
    ).grid(row=1, column=0, sticky="w", pady=(0, 6))

    # Formulaire
    form_card = ctk.CTkFrame(container, corner_radius=16)
    form_card.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 8))
    form_card.grid_columnconfigure(0, weight=0)
    form_card.grid_columnconfigure(1, weight=1)

    var_mode = ctk.StringVar(value="Classless (CIDR)")

    ctk.CTkLabel(form_card, text="Adresse IP", font=("Segoe UI", 15)).grid(
        row=0, column=0, sticky="e", padx=(16, 10), pady=(16, 8)
    )
    entry_ip = ctk.CTkEntry(
        form_card, placeholder_text="ex : 192.168.1.42", height=36
    )
    entry_ip.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=(16, 8))

    ctk.CTkLabel(form_card, text="Masque", font=("Segoe UI", 15)).grid(
        row=1, column=0, sticky="e", padx=(16, 10), pady=8
    )
    entry_mask = ctk.CTkEntry(
        form_card, placeholder_text="ex : /24 ou /255.255.255.0", height=36
    )
    entry_mask.grid(row=1, column=1, sticky="ew", padx=(0, 16), pady=8)

    ctk.CTkLabel(form_card, text="Mode", font=("Segoe UI", 15)).grid(
        row=2, column=0, sticky="e", padx=(16, 10), pady=8
    )
    seg_mode = ctk.CTkSegmentedButton(
        form_card,
        values=["Classless (CIDR)", "Classful"],
        variable=var_mode,
        font=ctk.CTkFont(size=15, weight="bold"),
    )
    seg_mode.set("Classless (CIDR)")
    seg_mode.grid(row=2, column=1, sticky="w", padx=(0, 16), pady=8)

    # Boutons d'action
    actions = ctk.CTkFrame(container, corner_radius=12)
    actions.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
    actions.grid_columnconfigure(0, weight=1)
    actions.grid_columnconfigure(1, weight=1)

    ctk.CTkButton(
        actions,
        text="Calculer",
        command=calculer,
        height=44,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    ).grid(row=0, column=0, sticky="ew", padx=6, pady=8)

    ctk.CTkButton(
        actions,
        text="Retour menu",
        command=lambda: page_menu(root),
        height=44,
        corner_radius=10,
        fg_color=DANGER,
        hover_color=DANGER_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    ).grid(row=0, column=1, sticky="ew", padx=6, pady=8)

    # Résultats
    result_card = ctk.CTkFrame(container, corner_radius=16)
    result_card.grid(row=3, column=0, sticky="nsew", padx=16, pady=(8, 16))
    result_card.grid_rowconfigure(1, weight=1)
    result_card.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        result_card,
        text="Résultat du calcul",
        font=("Segoe UI", 18, "bold"),
        justify="left",
    ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 0))

    text_result = ctk.CTkTextbox(result_card, corner_radius=8, wrap="word", font=("Consolas", 13))
    text_result.grid(row=1, column=0, sticky="nsew", padx=12, pady=(8, 12))
    text_result.configure(state="disabled")