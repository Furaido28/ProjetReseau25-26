from tkinter import messagebox
import customtkinter as ctk
import tkinter.ttk as ttk

from controllers.NetworkService import NetworkService
from views.pages.page_menu import page_menu
from views.utils.tools import clear_root, show_custom_message, show_input_dialog

network_service = NetworkService()

def page_decoupe_mode(root):
    clear_root(root)

    def verifier():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        mode = var_mode.get()

        if not ip or not mask or not val:
            show_custom_message("Erreur", "IP, Masque et Valeur sont obligatoires.", "error")
            return

        if not mask.startswith("/"):
            show_custom_message("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0", "error")
            return

        mask = mask[1:]

        try:
            val = int(val)
            if val <= 0:
                raise ValueError
        except ValueError:
            show_custom_message("Erreur", "La valeur doit être un entier positif.", "error")
            return

        try:
            ip_cidr = f"{ip}/{mask}"
            if mode == "nb_sr":
                report = network_service.verify_decoupe_possible(ip_cidr, nb_sr=val)
            else:
                report = network_service.verify_decoupe_possible(ip_cidr, nb_ips=val)

            if report.startswith("✅"):
                show_custom_message("Vérification réussie", report, "success")
            elif report.startswith("❌"):
                show_custom_message("Vérification impossible", report, "error")
            else:
                show_custom_message("Information", report, "info")
        except Exception as e:
            show_custom_message("Erreur", str(e), "error")

    def calculer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        mode = var_mode.get()

        if not ip or not mask or not val:
            messagebox.showerror("Erreur", "IP, Masque et Valeur sont obligatoires.")
            return

        if not mask.startswith("/"):
            messagebox.showerror("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0")
            return

        mask = mask[1:]

        try:
            val = int(val)
            if val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "La valeur doit être un entier positif.")
            return

        try:
            ip_cidr = f"{ip}/{mask}"
            if mode == "nb_sr":
                report = network_service.compute_subnets_choice(ip_cidr, nb_sr=val)
            else:
                report = network_service.compute_subnets_choice(ip_cidr, nb_ips=val)

            # Vide le tableau avant rechargement
            for item in tree.get_children():
                tree.delete(item)

            # Extraction et affichage des résultats
            lines = [l for l in report.splitlines() if l and not l.startswith("---")]
            sr, net, mask_val, first, last, bc, nb = [""] * 7
            for l in lines:
                if l.startswith("SR"):
                    if sr:
                        tree.insert("", "end", values=(sr, net, mask_val, first, last, bc, nb))
                    sr = l.split(":")[0]
                elif "Adresse réseau" in l:
                    net = l.split(":")[1].strip()
                elif "Masque" in l:
                    mask_val = l.split(":")[1].strip()
                elif "Première" in l:
                    first = l.split(":")[1].strip()
                elif "Dernière" in l:
                    last = l.split(":")[1].strip()
                elif "broadcast" in l:
                    bc = l.split(":")[1].strip()
                elif "Nb total" in l:
                    nb = l.split(":")[1].strip()
            if sr:
                tree.insert("", "end", values=(sr, net, mask_val, first, last, bc, nb))
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def enregistrer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        mode = var_mode.get()
        value = entry_value.get().strip()

        # validations
        if not ip or not mask:
            show_custom_message("Erreur", "IP et masque sont obligatoires pour enregistrer.", "error")
            return

        if not mask.startswith("/"):
            show_custom_message("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0", "error")
            return

        # normaliser le masque (on enlève le "/")
        mask_clean = mask[1:].strip()

        # récupérer le nom via ta input box CTk
        name = show_input_dialog("Nom de découpe", "Veuillez entrer le nom de la découpe :")
        if not name:
            show_custom_message("Info", "Enregistrement annulé.", "info")
            return

        responsable = getattr(root, "current_user", None) or "invité"

        try:
            # import local pour éviter les imports cycliques
            from repository.DecoupeRepository import DecoupeRepository

            repo = DecoupeRepository()

            # ✅ insertion directe sans objet métier
            decoupe_id = repo.insert_decoupe(
                name=name.strip(),
                responsable=responsable,
                base_ip=ip,
                base_mask=mask_clean,
                mode=mode,
                value=value,
            )

            show_custom_message("Succès", f"Découpe enregistrée (ID: {decoupe_id})", "success")

        except ValueError as ve:
            show_custom_message("Erreur", str(ve), "error")
        except Exception as e:
            show_custom_message("Erreur", f"Impossible d'enregistrer la découpe : {e}", "error")

    # --- LAYOUT ---
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Découpe réseau", font=("Arial", 20, "bold")).pack(pady=15)

    form_frame = ctk.CTkFrame(frame)
    form_frame.pack(fill="x", padx=20, pady=6)

    row1 = ctk.CTkFrame(form_frame)
    row1.pack(pady=6, fill="x")
    ctk.CTkLabel(row1, text="IP réseau").grid(row=0, column=0, padx=(0, 6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.0.0", height=30)
    entry_ip.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    row2 = ctk.CTkFrame(form_frame)
    row2.pack(pady=6, fill="x")
    ctk.CTkLabel(row2, text="Masque").grid(row=0, column=0, padx=(0, 6))
    entry_mask = ctk.CTkEntry(row2, placeholder_text="ex: /24 ou /255.255.255.0", height=30)
    entry_mask.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    var_mode = ctk.StringVar(value="nb_ips")
    row3 = ctk.CTkFrame(form_frame)
    row3.pack(pady=6)
    ctk.CTkRadioButton(row3, text="Par nombre d'IPs / SR", variable=var_mode, value="nb_ips").pack(side="left", padx=8)
    ctk.CTkRadioButton(row3, text="Par nombre de sous-réseaux", variable=var_mode, value="nb_sr").pack(side="left", padx=8)

    row4 = ctk.CTkFrame(form_frame)
    row4.pack(pady=6, fill="x")
    ctk.CTkLabel(row4, text="Valeur").grid(row=0, column=0, padx=(0, 6))
    entry_value = ctk.CTkEntry(row4, placeholder_text="ex: 8", height=30)
    entry_value.grid(row=0, column=1, sticky="ew")
    row4.grid_columnconfigure(1, weight=1)

    buttons_row = ctk.CTkFrame(frame)
    buttons_row.pack(pady=(6, 0), fill="x", padx=40)
    for i, (t, c) in enumerate([("Vérifier", verifier), ("Calculer", calculer), ("Enregistrer", enregistrer)]):
        ctk.CTkButton(buttons_row, text=t, command=c, height=40).grid(row=0, column=i, sticky="ew", padx=4, pady=6)
        buttons_row.grid_columnconfigure(i, weight=1)

    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root),
                  height=40).pack(pady=(10, 10), fill="x", padx=40)

    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=10, pady=10)

    columns = ("SR", "Réseau", "Masque", "1ère IP", "Dernière IP", "Broadcast", "Nb IPs")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(expand=True, fill="both", padx=10, pady=10)