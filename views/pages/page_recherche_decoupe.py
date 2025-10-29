import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox

from views.utils.clearRoot import clear_root
from views.utils.showCustomMessage import show_custom_message
from views.utils.showInputDialog import show_input_dialog
from views.pages.page_menu import page_menu


def page_recherche_decoupe(root):
    """Page de recherche de découpe réseau (par nom, filtrée par responsable connecté)."""

    # --------------------------- CONFIG & STYLE ---------------------------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    clear_root(root)
    root.geometry("1200x700")

    PRIMARY = "#34A853"
    PRIMARY_HOVER = "#2C8E47"

    username = getattr(root, "current_user", None) or "invité"

    # --------------------------- LAYOUT ----------------------------
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(root, corner_radius=16)
    container.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
    container.grid_rowconfigure(0, weight=0)  # header
    container.grid_rowconfigure(1, weight=0)  # form
    container.grid_rowconfigure(2, weight=1)  # result
    container.grid_rowconfigure(3, weight=0)  # footer
    container.grid_columnconfigure(0, weight=1)

    # --------------------------- HEADER ---------------------------
    header = ctk.CTkFrame(container, corner_radius=16)
    header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text="Recherche de découpe réseau",
        font=("Segoe UI", 25, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(6, 0))

    ctk.CTkLabel(
        header,
        text="Recherchez une découpe enregistrée par son nom. Seules vos découpes seront affichées.",
        font=("Segoe UI", 20),
        wraplength=1000,
        justify="left"
    ).grid(row=1, column=0, sticky="w", pady=(0, 6))

    # --------------------------- FORMULAIRE ---------------------------
    form_card = ctk.CTkFrame(container, corner_radius=16)
    form_card.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 8))
    form_card.grid_columnconfigure(0, weight=0)
    form_card.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        form_card,
        text="Nom de la découpe",
        font=("Segoe UI", 15)
    ).grid(row=0, column=0, sticky="e", padx=(16, 10), pady=10)

    entry_nom = ctk.CTkEntry(
        form_card,
        placeholder_text="ex: Découpe Bureaux Paris",
        height=36
    )
    entry_nom.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=10)

    # Le bouton Rechercher va filtrer le tableau selon l'entrée texte
    # mais ne va pas toucher aux autres découpes du user
    btn_rechercher = ctk.CTkButton(
        form_card,
        text="Rechercher",
        height=40,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold")
    )
    btn_rechercher.grid(row=0, column=2, padx=(10, 16), pady=10)

    # --------------------------- TABLEAU ---------------------------
    result_card = ctk.CTkFrame(container, corner_radius=16)
    result_card.grid(row=2, column=0, sticky="nsew", padx=16, pady=(8, 16))
    result_card.grid_rowconfigure(0, weight=1)
    result_card.grid_columnconfigure(0, weight=1)

    columns = ("ID", "Nom", "IP", "Masque", "Mode", "Valeur", "Responsable")

    style = ttk.Style()
    style.configure("Modern.Treeview", font=("Segoe UI", 16), rowheight=60)
    style.configure("Modern.Treeview.Heading", font=("Segoe UI Semibold", 13, "bold"))
    style.map(
        "Treeview",
        background=[('selected', PRIMARY)],
        foreground=[('selected', 'white')]
    )

    tree = ttk.Treeview(
        result_card,
        columns=columns,
        show="headings",
        style="Modern.Treeview"
    )
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=140, anchor="center")

    vsb = ttk.Scrollbar(
        result_card,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=vsb.set)

    tree.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12, 6))
    vsb.grid(row=0, column=1, sticky="ns", pady=(12, 6))

    # ---------------------------
    # FONCTIONS LIEES AU TABLEAU
    # ---------------------------

    def remplir_tableau(rows):
        """Vide le treeview puis insère les lignes fournies."""
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["name"],
                    row["base_ip"],
                    row["base_mask"],
                    row["mode"],
                    row["value"],
                    row["responsable"],
                ),
            )

    def charger_decoupes_utilisateur():
        """
        Charge toutes les découpes du user connecté
        et les affiche directement au lancement.
        """
        try:
            from repository.DecoupeRepository import DecoupeRepository
            repo = DecoupeRepository()
            rows = repo.list_by_responsable(username)  # uniquement ses découpes
            remplir_tableau(rows)
        except Exception as e:
            # si crash DB -> message d'erreur en toast + tableau vide
            remplir_tableau([])
            show_custom_message(
                "Erreur",
                f"Impossible de charger les découpes de {username} : {e}",
                "error"
            )

    def rechercher():
        """
        Filtre par nom dans les découpes de l'utilisateur.
        """
        name = entry_nom.get().strip()

        if not name:
            # champ vide -> on recharge juste toutes ses découpes
            charger_decoupes_utilisateur()
            show_custom_message(
                "Info",
                "Aucun filtre appliqué, affichage de toutes vos découpes.",
                "info"
            )
            return

        try:
            from repository.DecoupeRepository import DecoupeRepository
            repo = DecoupeRepository()

            rows = repo.list_by_responsable(username)  # toutes les siennes
            filtered_rows = [
                row for row in rows
                if name.lower() in row["name"].lower()
            ]

            remplir_tableau(filtered_rows)

            if not filtered_rows:
                show_custom_message(
                    "Résultat",
                    f"Aucune découpe trouvée contenant « {name} ».",
                    "info"
                )

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    # lier le vrai callback du bouton maintenant que rechercher() existe
    btn_rechercher.configure(command=rechercher)

    # ---------------------------
    # FOOTER
    # ---------------------------
    footer = ctk.CTkFrame(container, corner_radius=12)
    footer.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 16))
    for i in range(2):
        footer.grid_columnconfigure(i, weight=1)

    # Déclarer btn_modifier avant la fonction interne d'update
    btn_modifier = None

    def open_modifier_page():
        """Ouvre la page d'édition pour la découpe sélectionnée (si propriétaire)."""
        selected = tree.selection()
        if not selected:
            return
        item = tree.item(selected[0])
        decoupe_id = item["values"][0]  # ID dans la 1ère colonne

        from views.pages.page_modifier_decoupe import page_modifier_decoupe
        page_modifier_decoupe(root, decoupe_id)

    def update_btn_modifier_state(event=None):
        """
        Active le bouton 'Modifier' uniquement si la découpe appartient
        à l'utilisateur connecté.
        """
        if btn_modifier is None:
            return

        selected = tree.selection()
        if not selected:
            btn_modifier.configure(
                state="disabled",
                fg_color="#7F8C8D",
                hover_color="#7F8C8D",
            )
            return

        item = tree.item(selected[0])
        responsable = item["values"][6]  # colonne "Responsable"

        if responsable == username:
            btn_modifier.configure(
                state="normal",
                fg_color=PRIMARY,
                hover_color=PRIMARY_HOVER,
            )
        else:
            btn_modifier.configure(
                state="disabled",
                fg_color="#7F8C8D",
                hover_color="#7F8C8D",
            )

    btn_modifier = ctk.CTkButton(
        footer,
        text="Modifier",
        command=open_modifier_page,
        height=45,
        width=350,
        corner_radius=10,
        fg_color="#7F8C8D",
        hover_color="#7F8C8D",
        font=("Segoe UI Semibold", 18, "bold"),
        state="disabled"
    )
    btn_modifier.grid(row=0, column=0, padx=(10, 0), pady=12)

    ctk.CTkButton(
        footer,
        text="Retour menu",
        command=lambda: page_menu(root),
        height=45,
        width=350,
        corner_radius=10,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold")
    ).grid(row=0, column=1, pady=12)

    # Bind la sélection pour activer/désactiver "Modifier"
    tree.bind("<<TreeviewSelect>>", update_btn_modifier_state)

    # ---------------------------
    # CHARGEMENT INITIAL
    # ---------------------------
    charger_decoupes_utilisateur()