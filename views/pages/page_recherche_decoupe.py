import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox

from views.utils.clearRoot import clear_root
from views.utils.showCustomMessage import show_custom_message
from views.utils.showInputDialog import show_input_dialog
from views.pages.page_menu import page_menu
from views.utils.showQuestionDialog import show_question_dialog


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
    for i in range(3):
        footer.grid_columnconfigure(i, weight=1)

    # Déclarer les boutons avant les fonctions qui les manipulent
    btn_modifier = None
    btn_supprimer = None

    def open_modifier_page():
        """Ouvre la page d'édition pour la découpe sélectionnée (si propriétaire)."""
        selected = tree.selection()
        if not selected:
            return
        item = tree.item(selected[0])
        decoupe_id = item["values"][0]  # ID dans la 1ère colonne

        from views.pages.page_modifier_decoupe import page_modifier_decoupe
        page_modifier_decoupe(root, decoupe_id)

    def update_btn_states(event=None):
        """
        Active les boutons 'Modifier' et 'Supprimer' uniquement si la découpe
        appartient à l'utilisateur connecté.
        """
        if btn_modifier is None or btn_supprimer is None:
            return

        selected = tree.selection()
        if not selected:
            # Rien sélectionné → on désactive tout
            btn_modifier.configure(
                state="disabled",
                fg_color="#7F8C8D",
                hover_color="#7F8C8D",
            )
            btn_supprimer.configure(
                state="disabled",
                fg_color="#7F8C8D",
                hover_color="#7F8C8D",
            )
            return

        item = tree.item(selected[0])
        responsable = item["values"][6]  # colonne "Responsable"

        if responsable == username:
            # Propriétaire → on active les boutons
            btn_modifier.configure(
                state="normal",
                fg_color=PRIMARY,
                hover_color=PRIMARY_HOVER,
            )
            btn_supprimer.configure(
                state="normal",
                fg_color=PRIMARY,
                hover_color=PRIMARY_HOVER,
            )
        else:
            # Pas propriétaire → on désactive
            btn_modifier.configure(
                state="disabled",
                fg_color="#7F8C8D",
                hover_color="#7F8C8D",
            )
            btn_supprimer.configure(
                state="disabled",
                fg_color="#7F8C8D",
                hover_color="#7F8C8D",
            )

    def supprimer_decoupe():
        """Supprime la découpe sélectionnée si elle appartient à l'utilisateur."""
        selected = tree.selection()
        if not selected:
            show_custom_message("Erreur", "Aucune découpe sélectionnée.", "error")
            return

        item = tree.item(selected[0])
        decoupe_id = item["values"][0]
        nom_decoupe = item["values"][1]
        responsable = item["values"][6]

        # Vérifie que la découpe appartient bien à l'utilisateur connecté
        if responsable != username:
            show_custom_message(
                "Refusé",
                "Vous ne pouvez supprimer qu'une découpe dont vous êtes responsable.",
                "warning"
            )
            return

        # Demande de confirmation
        confirm = show_question_dialog(
            title="Confirmation",
            message=f"Voulez-vous vraiment supprimer la découpe « {nom_decoupe} » ?",
            button1_text="Oui",
            button2_text="Non"
        )

        if not confirm:
            return

        try:
            from repository.DecoupeRepository import DecoupeRepository
            repo = DecoupeRepository()
            repo.delete_decoupe(decoupe_id)

            # Rafraîchit la liste
            charger_decoupes_utilisateur()

            show_custom_message("Succès", "Découpe supprimée avec succès.", "success")

            # Après suppression, on désactive les boutons (plus de sélection valide)
            btn_modifier.configure(
                state="disabled",
                fg_color="#7F8C8D",
                hover_color="#7F8C8D",
            )
            btn_supprimer.configure(
                state="disabled",
                fg_color="#7F8C8D",
                hover_color="#7F8C8D",
            )

        except Exception as e:
            show_custom_message(
                "Erreur",
                f"Impossible de supprimer la découpe : {e}",
                "error"
            )

    # Bouton Modifier (désactivé par défaut)
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

    # Bouton Supprimer (désactivé par défaut)
    btn_supprimer = ctk.CTkButton(
        footer,
        text="Supprimer",
        command=supprimer_decoupe,
        height=45,
        width=350,
        corner_radius=10,
        fg_color="#7F8C8D",   # grisé au début
        hover_color="#7F8C8D",
        font=("Segoe UI Semibold", 18, "bold"),
        state="disabled"
    )
    btn_supprimer.grid(row=0, column=1, pady=12)

    # Bouton Retour menu
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
    ).grid(row=0, column=2, pady=12)

    # Bind la sélection pour activer/désactiver "Modifier" et "Supprimer"
    tree.bind("<<TreeviewSelect>>", update_btn_states)

    # ---------------------------
    # CHARGEMENT INITIAL
    # ---------------------------
    charger_decoupes_utilisateur()
    # Et on s'assure que les boutons sont bien désactivés au démarrage
    update_btn_states()