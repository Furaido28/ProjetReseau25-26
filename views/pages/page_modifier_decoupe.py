# views/pages/page_modifier_decoupe.py
from tkinter import messagebox
from typing import Optional
import customtkinter as ctk
import tkinter.ttk as ttk

from views.pages.page_menu import page_menu
from views.utils.tools import clear_root, show_custom_message
from repository.DecoupeRepository import DecoupeRepository
from controllers.NetworkService import NetworkService

network_service = NetworkService()


def page_modifier_decoupe(root, decoupe_id):
    """
    Page pour modifier une découpe existante.
    On peut modifier le masque, la valeur et le mode (nb_sr / nb_ips).
    """

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    clear_root(root)
    root.geometry("1200x700")

    PRIMARY = "#34A853"
    PRIMARY_HOVER = "#2C8E47"
    DISABLED = "#7F8C8D"

    repo = DecoupeRepository()
    username = getattr(root, "current_user", None) or "invité"

    # Charger la découpe depuis la BDD
    decoupe = repo.get_decoupe_by_id(decoupe_id)
    if not decoupe:
        messagebox.showerror("Erreur", "Découpe introuvable.")
        page_menu(root)
        return

    if decoupe["responsable"] != username:
        messagebox.showerror("Erreur", "Vous n'êtes pas autorisé à modifier cette découpe.")
        page_menu(root)
        return

    # ---------------------------
    # Helpers pour boutons
    # ---------------------------
    def set_btn_disabled(btn):
        btn.configure(state="disabled", fg_color=DISABLED, hover_color=DISABLED)

    def set_btn_enabled(btn):
        btn.configure(state="normal", fg_color=PRIMARY, hover_color=PRIMARY_HOVER)

    def disable_calc_and_modify():
        set_btn_disabled(btn_calculer)
        set_btn_disabled(btn_modifier)

    # ---------------------------
    # Logique
    # ---------------------------
    def verifier() -> Optional[bool]:
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        ip = decoupe["base_ip"]
        mode_label = var_mode.get()

        # Normaliser le mode en "nb_sr" ou "nb_ips"
        if mode_label == "nombre de sous-réseau":
            mode = "nb_sr"
        else:
            mode = "nb_ips"

        if not mask or not val:
            show_custom_message("Erreur", "Masque et Valeur sont obligatoires.", "error")
            return False
        if not mask.startswith("/"):
            show_custom_message("Erreur", "Le masque doit commencer par '/'. Exemple : /24", "error")
            return False
        try:
            val_int = int(val)
            if val_int <= 0:
                raise ValueError
        except ValueError:
            show_custom_message("Erreur", "La valeur doit être un entier positif.", "error")
            return False

        mask_clean = mask[1:]
        ip_cidr = f"{ip}/{mask_clean}"
        try:
            if mode == "nb_sr":
                report = network_service.verify_decoupe_possible(ip_cidr, nb_sr=val_int)
            else:
                report = network_service.verify_decoupe_possible(ip_cidr, nb_ips=val_int)

            if isinstance(report, str) and report.startswith("✅"):
                show_custom_message("Vérification réussie", report, "success")
                return True
            elif isinstance(report, str) and report.startswith("❌"):
                show_custom_message("Vérification impossible", report, "error")
            else:
                # message neutre / info
                show_custom_message("Info", report if isinstance(report, str) else str(report), "info")
            return False
        except Exception as e:
            show_custom_message("Erreur", str(e), "error")
            return False

    def calculer():
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        ip = decoupe["base_ip"]
        mode_label = var_mode.get()
        mode = "nb_sr" if mode_label == "nombre de sous-réseau" else "nb_ips"

        mask_clean = mask[1:]
        val_int = int(val)
        ip_cidr = f"{ip}/{mask_clean}"

        if mode == "nb_sr":
            report = network_service.compute_subnets_choice(ip_cidr, nb_sr=val_int)
        else:
            report = network_service.compute_subnets_choice(ip_cidr, nb_ips=val_int)

        # vider le tableau
        for item in tree.get_children():
            tree.delete(item)

        # afficher le résultat
        lines = [l for l in report.splitlines() if l and not l.startswith("---")]
        sr, net, mask_val, first, last, bc, nb = [""] * 7
        for l in lines:
            if l.startswith("SR"):
                if sr:
                    tree.insert("", "end", values=(sr, net, mask_val, first, last, bc, nb))
                sr = l.split(":")[0]
            elif "Adresse réseau" in l:
                parts = l.split(":", 1)
                net = parts[1].strip() if len(parts) > 1 else ""
            elif "Masque" in l:
                parts = l.split(":", 1)
                mask_val = parts[1].strip() if len(parts) > 1 else ""
            elif "Première" in l:
                parts = l.split(":", 1)
                first = parts[1].strip() if len(parts) > 1 else ""
            elif "Dernière" in l:
                parts = l.split(":", 1)
                last = parts[1].strip() if len(parts) > 1 else ""
            elif "broadcast" in l:
                parts = l.split(":", 1)
                bc = parts[1].strip() if len(parts) > 1 else ""
            elif "Nb total" in l:
                parts = l.split(":", 1)
                nb = parts[1].strip() if len(parts) > 1 else ""
        if sr:
            tree.insert("", "end", values=(sr, net, mask_val, first, last, bc, nb))

        set_btn_enabled(btn_modifier)

    def modifier():
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        mode_label = var_mode.get()
        mode = "nb_sr" if mode_label == "nombre de sous-réseau" else "nb_ips"

        try:
            repo.update_decoupe(decoupe_id, base_mask=mask[1:], value=val, mode=mode)
            show_custom_message("Succès", "Découpe modifiée avec succès.", "success")
            # Optionnel: revenir au menu principal
            page_menu(root)
        except Exception as e:
            show_custom_message("Erreur", f"Impossible de modifier la découpe : {e}", "error")

    def verifier_and_enable_next():
        isOK = verifier()

        if not isOK:
            return

        # Si la vérification réussit => on rend Calculer cliquable et vert
        set_btn_enabled(btn_calculer)

    def calculer_and_enable_next():
        calculer()

        # Afficher le résultat => on rend Calculer cliquable et vert
        set_btn_enabled(btn_calculer)

    # ---------------------------
    # Layout
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

    # Header
    header = ctk.CTkFrame(container, corner_radius=16)
    header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
    header.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(header, text="Modifier découpe réseau", font=("Segoe UI", 22, "bold")).grid(row=0, column=0, sticky="w", pady=(6, 0))
    ctk.CTkLabel(
        header,
        text="Vous pouvez modifier le masque, la valeur et le mode de la découpe.",
        font=("Segoe UI", 13),
        wraplength=1000,
        justify="left"
    ).grid(row=1, column=0, sticky="w", pady=(0, 6))

    # Formulaire
    form_card = ctk.CTkFrame(container, corner_radius=16)
    form_card.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 8))
    form_card.grid_columnconfigure(0, weight=0)
    form_card.grid_columnconfigure(1, weight=1)

    var_mask = ctk.StringVar(value="/" + str(decoupe["base_mask"]))
    var_value = ctk.StringVar(value=str(decoupe["value"]))
    # Adapter le label du segmented button à partir du mode en base
    mode_label = "nombre d'ip total" if decoupe["mode"] == "nb_ips" else "nombre de sous-réseau"
    var_mode = ctk.StringVar(value=mode_label)

    ctk.CTkLabel(form_card, text="Nom (non modifiable)", font=("Segoe UI", 13)).grid(row=0, column=0, sticky="e", padx=(16, 10), pady=10)
    entry_name = ctk.CTkEntry(form_card, placeholder_text="Nom de la découpe", height=36)
    entry_name.insert(0, decoupe["name"])
    entry_name.configure(state="disabled")
    entry_name.grid(row=0, column=1, sticky="ew", padx=(0,16), pady=10)

    # Mode (Segmented button identique à page_decoupe_mode)
    ctk.CTkLabel(form_card, text="Mode", font=("Segoe UI", 13)).grid(row=1, column=0, sticky="e", padx=(16,10), pady=10)
    seg_mode = ctk.CTkSegmentedButton(
        form_card,
        values=["nombre d'ip total", "nombre de sous-réseau"],
        variable=var_mode,
        font=ctk.CTkFont(size=13, weight="bold"),

        text_color="white",
        text_color_disabled="white",

        fg_color="#979DA2",
        selected_color=PRIMARY,
        selected_hover_color=PRIMARY_HOVER,
        unselected_color="#979DA2",
        unselected_hover_color="#B3B3B3"
    )
    seg_mode.set(mode_label)
    seg_mode.grid(row=1, column=1, sticky="w", padx=(0,16), pady=10)

    ctk.CTkLabel(form_card, text="Masque", font=("Segoe UI", 13)).grid(row=2, column=0, sticky="e", padx=(16,10), pady=10)
    entry_mask = ctk.CTkEntry(form_card, textvariable=var_mask, placeholder_text="ex: /24", height=36)
    entry_mask.grid(row=2, column=1, sticky="ew", padx=(0,16), pady=10)

    ctk.CTkLabel(form_card, text="Valeur", font=("Segoe UI", 13)).grid(row=3, column=0, sticky="e", padx=(16,10), pady=10)
    entry_value = ctk.CTkEntry(form_card, textvariable=var_value, placeholder_text="ex: 8", height=36)
    entry_value.grid(row=3, column=1, sticky="ew", padx=(0,16), pady=10)

    # Actions
    actions = ctk.CTkFrame(container, corner_radius=12)
    actions.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
    for i in range(4):
        actions.grid_columnconfigure(i, weight=1)

    btn_verifier = ctk.CTkButton(
        actions, text="Vérifier", command=lambda: verifier_and_enable_next(),
        height=44, corner_radius=10,
        fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 15, "bold"),
    )
    btn_verifier.grid(row=0, column=0, sticky="ew", padx=6, pady=8)

    btn_calculer = ctk.CTkButton(
        actions, text="Calculer", command=lambda: calculer_and_enable_next(),
        height=44, corner_radius=10,
        fg_color=DISABLED, hover_color=DISABLED,
        font=("Segoe UI Semibold", 15, "bold"),
        state="disabled"
    )
    btn_calculer.grid(row=0, column=1, sticky="ew", padx=6, pady=8)

    btn_modifier = ctk.CTkButton(
        actions, text="Modifier", command=modifier,
        height=44, corner_radius=10,
        fg_color=DISABLED, hover_color=DISABLED,
        font=("Segoe UI Semibold", 15, "bold"),
        state="disabled"
    )
    btn_modifier.grid(row=0, column=2, sticky="ew", padx=6, pady=8)

    btn_retour = ctk.CTkButton(actions, text="Retour menu", command=lambda: page_menu(root), height=44, corner_radius=10, fg_color=PRIMARY, hover_color=PRIMARY_HOVER, font=("Segoe UI Semibold", 15, "bold"))
    btn_retour.grid(row=0, column=3, sticky="ew", padx=6, pady=8)

    # Résultats
    result_card = ctk.CTkFrame(container, corner_radius=16)
    result_card.grid(row=3, column=0, sticky="nsew", padx=16, pady=(8,16))
    result_card.grid_rowconfigure(0, weight=1)
    result_card.grid_columnconfigure(0, weight=1)

    columns = ("SR", "Réseau", "Masque", "1ère IP", "Dernière IP", "Broadcast", "Nb IPs")
    style = ttk.Style()
    style.configure("Modern.Treeview", font=("Segoe UI", 11), rowheight=28)
    style.configure("Modern.Treeview.Heading", font=("Segoe UI Semibold", 13, "bold"))
    tree = ttk.Treeview(result_card, columns=columns, show="headings", style="Modern.Treeview")
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=150, anchor="center")

    vsb = ttk.Scrollbar(result_card, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12,6))
    vsb.grid(row=0, column=1, sticky="ns", pady=(12,6))

    # Désactiver les boutons si modification dans les champs
    def on_change(*_):
        disable_calc_and_modify()
        for item in tree.get_children():
            tree.delete(item)
    var_mask.trace_add("write", on_change)
    var_value.trace_add("write", on_change)
    var_mode.trace_add("write", on_change)
    seg_mode.configure(command=lambda _: on_change())

    # si l'utilisateur modifie via clavier (coller etc.)
    entry_mask.bind("<KeyRelease>", lambda e: on_change())
    entry_value.bind("<KeyRelease>", lambda e: on_change())

    # Fin de la page
