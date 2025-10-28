# views/pages/page_recherche_decoupe.py
import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox

from views.utils.tools import clear_root, show_custom_message
from views.pages.page_menu import page_menu


def page_recherche_decoupe(root):
    """Page de recherche de découpe réseau (par nom, filtrée par responsable connecté)."""

    # --------------------------- CONFIG & STYLE ---------------------------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    clear_root(root)
    root.geometry("1200x700")

    PRIMARY = "#2ECC71"
    PRIMARY_HOVER = "#27AE60"
    DANGER = "#E74C3C"
    DANGER_HOVER = "#C0392B"

    username = getattr(root, "current_user", None) or "invité"

    # --------------------------- LOGIQUE DE RECHERCHE ---------------------------
    def rechercher():
        """Recherche SQL par nom + responsable connecté."""
        name = entry_nom.get().strip()
        if not name:
            show_custom_message("Information", "Veuillez entrer un nom de découpe à rechercher.", "info")
            return

        try:
            from repository.DecoupeRepository import DecoupeRepository
            repo = DecoupeRepository()
            # Recherche uniquement sur le nom, toutes les découpes
            rows = repo.list_by_responsable(username)
            filtered_rows = [row for row in rows if name.lower() in row["name"].lower()]

            # Nettoyage du tableau
            for item in tree.get_children():
                tree.delete(item)

            if not rows:
                show_custom_message("Résultat", f"Aucune découpe trouvée pour '{name}' appartenant à {username}.", "info")
                return

            # Remplissage du tableau
            for row in filtered_rows:
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
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

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

    ctk.CTkLabel(header, text="Recherche de découpe réseau", font=("Segoe UI", 25, "bold")).grid(row=0, column=0, sticky="w", pady=(6, 0))
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

    ctk.CTkLabel(form_card, text="Nom de la découpe", font=("Segoe UI", 15)).grid(row=0, column=0, sticky="e", padx=(16, 10), pady=10)
    entry_nom = ctk.CTkEntry(form_card, placeholder_text="ex: Découpe Bureaux Paris", height=36)
    entry_nom.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=10)

    btn_rechercher = ctk.CTkButton(
        form_card,
        text="Rechercher",
        command=rechercher,
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

    tree = ttk.Treeview(result_card, columns=columns, show="headings", style="Modern.Treeview")
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=140, anchor="center")

    vsb = ttk.Scrollbar(result_card, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12, 6))
    vsb.grid(row=0, column=1, sticky="ns", pady=(12, 6))

    # --------------------------- FOOTER ---------------------------
    footer = ctk.CTkFrame(container, corner_radius=12)
    footer.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 16))
    for i in range(2):
        footer.grid_columnconfigure(i, weight=1)

    # Déclarer btn_modifier avant la fonction pour éviter l'erreur
    btn_modifier = None

    # Callback pour ouvrir la page de modification
    def open_modifier_page():
        selected = tree.selection()
        if not selected:
            return
        item = tree.item(selected[0])
        decoupe_id = item["values"][0]  # ID de la découpe
        from views.pages.page_modifier_decoupe import page_modifier_decoupe
        page_modifier_decoupe(root, decoupe_id)

    # Fonction pour activer/désactiver le bouton selon le responsable
    def update_btn_modifier_state(event=None):
        if btn_modifier is None:
            return
        selected = tree.selection()
        if not selected:
            btn_modifier.configure(state="disabled")
            return
        item = tree.item(selected[0])
        responsable = item["values"][6]  # colonne Responsable
        if responsable == username:
            btn_modifier.configure(state="normal", fg_color="#2ECC71", hover_color="#27AE60")
        else:
            btn_modifier.configure(state="disabled")

    # Création du bouton Modifier
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

    # Bouton Retour menu
    ctk.CTkButton(
        footer,
        text="Retour menu",
        command=lambda: page_menu(root),
        height=45,
        width=350,
        corner_radius=10,
        fg_color=DANGER,
        hover_color=DANGER_HOVER,
        font=("Segoe UI Semibold", 18, "bold")
    ).grid(row=0, column=1, pady=12)

    # Bind pour activer/désactiver le bouton Modifier lors de la sélection
    tree.bind("<<TreeviewSelect>>", update_btn_modifier_state)
