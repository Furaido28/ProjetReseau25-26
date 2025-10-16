import customtkinter as ctk

from controllers.NetworkService import NetworkService
from views.pages.page_menu import page_menu
from views.utils.tools import clear_root, show_custom_message

network_service = NetworkService()

MAX_SR = 100
NB_COLS = 3  # Nombre de colonnes pour limiter le défilement


def page_verif_decoupe_vlsm(root):
    # ---------------------------
    # THÈME / FENÊTRE
    # ---------------------------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    clear_root(root)
    root.geometry("1250x700")

    # ---------------------------
    # COULEURS / STYLE (aligné)
    # ---------------------------
    PRIMARY = "#2ECC71"
    PRIMARY_HOVER = "#27AE60"
    DANGER = "#E74C3C"
    DANGER_HOVER = "#C0392B"

    # ---------------------------
    # LAYOUT VERTICAL (header, form, actions, dynamic)
    # ---------------------------
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(root, corner_radius=16)
    container.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
    container.grid_rowconfigure(0, weight=0)  # header
    container.grid_rowconfigure(1, weight=0)  # form
    container.grid_rowconfigure(2, weight=0)  # actions
    container.grid_rowconfigure(3, weight=1)  # dynamic scroll area
    container.grid_columnconfigure(0, weight=1)

    # En-tête
    header = ctk.CTkFrame(container, corner_radius=16)
    header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text="Vérification découpe VLSM",
        font=("Segoe UI", 25, "bold"),
    ).grid(row=0, column=0, sticky="w", pady=(6, 0))

    ctk.CTkLabel(
        header,
        text=(
            "Cette page vérifie si une découpe VLSM est possible pour un réseau donné "
            "et vos besoins en nombre d'hôtes par sous-réseau."
        ),
        font=("Segoe UI", 20),
        wraplength=1150,
        justify="left",
    ).grid(row=1, column=0, sticky="w", pady=(0, 6))

    # Formulaire
    form_card = ctk.CTkFrame(container, corner_radius=16)
    form_card.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 8))
    form_card.grid_columnconfigure(0, weight=0)
    form_card.grid_columnconfigure(1, weight=1)
    form_card.grid_columnconfigure(2, weight=0)

    # Ligne IP réseau
    ctk.CTkLabel(form_card, text="IP réseau", font=("Segoe UI", 15)).grid(
        row=0, column=0, sticky="e", padx=(16, 10), pady=(16, 8)
    )
    entry_network = ctk.CTkEntry(
        form_card, placeholder_text="ex : 192.168.0.0", height=36
    )
    entry_network.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=(16, 8))

    # Ligne Masque
    ctk.CTkLabel(form_card, text="Masque", font=("Segoe UI", 15)).grid(
        row=1, column=0, sticky="e", padx=(16, 10), pady=8
    )
    entry_mask = ctk.CTkEntry(
        form_card, placeholder_text="ex : /24 ou /255.255.255.0", height=36
    )
    entry_mask.grid(row=1, column=1, sticky="ew", padx=(0, 16), pady=8)

    # Ligne Nombre de SR + bouton Générer
    ctk.CTkLabel(form_card, text="Nombre de sous-réseaux", font=("Segoe UI", 15)).grid(
        row=2, column=0, sticky="e", padx=(16, 10), pady=8
    )
    entry_subnet_count = ctk.CTkEntry(
        form_card, placeholder_text=f"1 à {MAX_SR}", height=36
    )
    entry_subnet_count.grid(row=2, column=1, sticky="ew", padx=(0, 8), pady=8)

    btn_generer_inline = ctk.CTkButton(
        form_card,
        text="Générer",
        height=36,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 16, "bold"),
    )
    btn_generer_inline.grid(row=2, column=2, sticky="w", padx=(0, 16), pady=8)

    # Actions (barre)
    actions = ctk.CTkFrame(container, corner_radius=12)
    actions.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
    actions.grid_columnconfigure(0, weight=1)
    actions.grid_columnconfigure(1, weight=1)

    btn_verifier = ctk.CTkButton(
        actions,
        text="Vérifier",
        height=44,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    )
    btn_verifier.grid(row=0, column=0, sticky="ew", padx=6, pady=8)

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

    # Conteneur scrollable pour les champs dynamiques
    dynamic_card = ctk.CTkFrame(container, corner_radius=16)
    dynamic_card.grid(row=3, column=0, sticky="nsew", padx=16, pady=(8, 16))
    dynamic_card.grid_rowconfigure(0, weight=1)
    dynamic_card.grid_columnconfigure(0, weight=1)

    scroll = ctk.CTkScrollableFrame(dynamic_card)
    scroll.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

    for col in range(NB_COLS):
        scroll.grid_columnconfigure(col, weight=1, uniform="cols")

    # Stockage des entrées dynamiques
    subnet_entries = []  # Chaque item: {"name": "SR 1", "hosts_entry": <CTkEntry>}

    def generer_champs():
        # Nettoyage total de la zone scrollable
        for child in scroll.winfo_children():
            child.destroy()
        subnet_entries.clear()

        # Validation count
        raw = entry_subnet_count.get().strip()
        if not raw:
            show_custom_message("Erreur", "Veuillez indiquer un nombre de sous-réseaux.", "error")
            return
        try:
            n = int(raw)
        except ValueError:
            show_custom_message("Erreur", "Le nombre de sous-réseaux doit être un entier.", "error")
            return
        if n <= 0:
            show_custom_message("Attention", "Le nombre doit être supérieur à 0.", "info")
            return
        if n > MAX_SR:
            show_custom_message("Limite", f"Maximum {MAX_SR} sous-réseaux. La valeur sera réduite à {MAX_SR}.", "info")
            n = MAX_SR

        # Génération des cartes sur NB_COLS colonnes
        for i in range(n):
            r, c = divmod(i, NB_COLS)
            card = ctk.CTkFrame(scroll, corner_radius=12)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

            # En-tête (numéro SR)
            sr_name = f"SR {i+1}"
            ctk.CTkLabel(card, text=sr_name, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 6))

            # Uniquement "Hôtes requis"
            row_hosts = ctk.CTkFrame(card)
            row_hosts.pack(fill="x", padx=10, pady=(0, 12))
            ctk.CTkLabel(row_hosts, text="Hôtes requis", font=("Segoe UI", 13)).grid(row=0, column=0, padx=(0, 6))
            hosts_entry = ctk.CTkEntry(row_hosts, placeholder_text="ex : 50", height=32)
            hosts_entry.grid(row=0, column=1, sticky="ew")
            row_hosts.grid_columnconfigure(1, weight=1)

            subnet_entries.append({"name": sr_name, "hosts_entry": hosts_entry})

    # Associer le bouton inline "Générer"
    btn_generer_inline.configure(command=generer_champs)

    # Vérification VLSM
    def verifier_action():
        network = entry_network.get().strip()
        mask = entry_mask.get().strip()
        if not network or not mask:
            show_custom_message("Erreur", "Veuillez saisir l'IP réseau et le masque.", "error")
            return
        if not mask.startswith("/"):
            show_custom_message(
                "Erreur",
                "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0",
                "error",
            )
            return

        besoins = []
        for item in subnet_entries:
            sr = item["name"]
            raw = item["hosts_entry"].get().strip()
            try:
                h = int(raw)
                if h < 1:
                    raise ValueError
            except ValueError:
                show_custom_message("Erreur", f"'{raw}' n'est pas un nombre d'hôtes valide pour {sr}.", "error")
                return
            besoins.append((sr, h))

        ok, msg, details = network_service.verify_vlsm(network, mask, besoins)
        if ok:
            lines = [msg, "-" * 50]
            for d in details:
                lines.append(f"{d['name']}: {d['hosts']} hôtes → bloc {d['block_size']} adresses (/{d['prefix']})")
            show_custom_message("Vérification VLSM", "\n".join(lines), "success")
        else:
            lines = [msg]
            if details:
                worst = min(details, key=lambda d: d["prefix"])  # plus gros besoin = plus petit prefix
                lines.append(
                    f"Plus gros besoin rencontré : {worst['name']} → /{worst['prefix']} ({worst['block_size']} adresses)."
                )
            show_custom_message("VLSM impossible", "\n".join(lines), "error")

    btn_verifier.configure(command=verifier_action)

    # Valeur par défaut et génération initiale
    entry_subnet_count.insert(0, "3")
    generer_champs()

