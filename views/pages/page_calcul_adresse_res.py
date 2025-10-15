from tkinter import messagebox
import customtkinter as ctk
import tkinter.ttk as ttk

from controllers.NetworkService import NetworkService
from views.pages.page_menu import page_menu
from views.utils.tools import clear_root

network_service = NetworkService()

def page_adresse_reseau(root):
    clear_root(root)

    def calculer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        mode = var_mode.get()

        if not ip:
            messagebox.showerror("Erreur", "L'adresse IP est obligatoire.")
            return

        if mode == "classless":
            if not mask:
                messagebox.showerror("Erreur", "Le masque est obligatoire en mode classless.")
                return
            if not mask.startswith("/"):
                messagebox.showerror("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0")
                return
            mask = mask[1:]  # retire le "/"

        if mode == "classful":
            if mask:
                if not mask.startswith("/"):
                    messagebox.showerror("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0")
                    return
                mask = mask[1:]  # retire le "/"

        try:
            is_classful = (mode == "classful")
            mask_to_use = mask if mask else None
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

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Calcul d’adresse réseau",
                 font=("Arial", 22, "bold")).pack(pady=(10, 20))

    form_frame = ctk.CTkFrame(frame, corner_radius=10)
    form_frame.pack(fill="x", padx=30, pady=(10, 10))

    def row(label, placeholder):
        row = ctk.CTkFrame(form_frame)
        row.pack(pady=8, fill="x")
        ctk.CTkLabel(row, text=label, font=("Arial", 13, "bold")).grid(row=0, column=0, padx=(0, 8))
        entry = ctk.CTkEntry(row, placeholder_text=placeholder, height=32)
        entry.grid(row=0, column=1, sticky="ew")
        row.grid_columnconfigure(1, weight=1)
        return entry

    entry_ip = row("Adresse IP :", "ex : 192.168.1.42")
    entry_mask = row("Masque :", "ex : /24 ou /255.255.255.0")

    var_mode = ctk.StringVar(value="classless")
    mode_row = ctk.CTkFrame(form_frame)
    mode_row.pack(pady=8)
    ctk.CTkRadioButton(mode_row, text="Classless (CIDR)", variable=var_mode, value="classless").pack(side="left", padx=10)
    ctk.CTkRadioButton(mode_row, text="Classful", variable=var_mode, value="classful").pack(side="left", padx=10)

    btns = ctk.CTkFrame(frame)
    btns.pack(fill="x", padx=40, pady=(10, 0))
    ctk.CTkButton(btns, text="Calculer", command=calculer, height=40).grid(row=0, column=0, sticky="ew", padx=(0, 8))
    ctk.CTkButton(btns, text="Retour menu", command=lambda: page_menu(root),
                  height=40).grid(row=0, column=1, sticky="ew", padx=(8, 0))
    btns.grid_columnconfigure(0, weight=1)
    btns.grid_columnconfigure(1, weight=1)

    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=25, pady=(10, 15))
    ctk.CTkLabel(result_frame, text="Résultat du calcul", font=("Arial", 14, "bold")).pack(pady=(10, 5))
    text_result = ctk.CTkTextbox(result_frame, corner_radius=8, wrap="word", font=("Consolas", 13))
    text_result.pack(expand=True, fill="both", padx=10, pady=(0, 10))