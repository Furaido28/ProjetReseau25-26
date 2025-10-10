from tkinter import messagebox
import customtkinter as ctk
import tkinter.ttk as ttk

from controllers.NetworkService import NetworkService
from views.pages.page_menu import page_menu
from views.utils.tools import clear_root

network_service = NetworkService()

def page_verif_adresse_reseau(root):
    clear_root(root)

    def verifier():
        ip = entry_ip.get().strip()
        network_ip = entry_network_ip.get().strip()
        network_mask = entry_network_mask.get().strip()

        if not ip or not network_ip or not network_mask:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        if not network_mask.startswith("/"):
            messagebox.showerror("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0")
            return

        network_mask = network_mask[1:]  # on retire le "/"

        result, first, last, error = network_service.define_ip_in_network(ip, network_ip, network_mask)

        text_result.configure(state="normal")
        text_result.delete("1.0", "end")

        if error:
            text_result.insert("end", f"Erreur : {error}")
        elif result:
            text_result.insert("end", f"✅ L'adresse IP {ip} appartient au réseau {network_ip}/{network_mask}\n\n")
            text_result.insert("end", f"Plage d'adresses : {first} → {last}")
        else:
            text_result.insert("end", f"❌ L'adresse IP {ip} n'appartient pas au réseau {network_ip}/{network_mask}")
        text_result.configure(state="disabled")

    # Interface
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Vérification d'une adresse IP dans un réseau",
                 font=("Arial", 22, "bold")).pack(pady=(10, 20))

    form_frame = ctk.CTkFrame(frame, corner_radius=10)
    form_frame.pack(fill="x", padx=25, pady=(5, 15))

    def make_row(parent, label, placeholder):
        row = ctk.CTkFrame(parent)
        row.pack(pady=8, fill="x")
        ctk.CTkLabel(row, text=label, font=("Arial", 13)).grid(row=0, column=0, padx=(0, 8))
        entry = ctk.CTkEntry(row, placeholder_text=placeholder, height=32)
        entry.grid(row=0, column=1, sticky="ew")
        row.grid_columnconfigure(1, weight=1)
        return entry

    entry_ip = make_row(form_frame, "IP à tester :", "ex : 192.168.1.42")
    entry_network_ip = make_row(form_frame, "IP réseau :", "ex : 192.168.1.0")
    entry_network_mask = make_row(form_frame, "Masque :", "ex : /24 ou /255.255.255.0")

    btns = ctk.CTkFrame(frame)
    btns.pack(fill="x", padx=40, pady=(5, 5))
    ctk.CTkButton(btns, text="Vérifier", command=verifier, height=40).grid(row=0, column=0, sticky="ew", padx=(0, 8))
    ctk.CTkButton(btns, text="Retour menu", command=lambda: page_menu(root),
                  height=40).grid(row=0, column=1, sticky="ew", padx=(8, 0))
    btns.grid_columnconfigure(0, weight=1)
    btns.grid_columnconfigure(1, weight=1)

    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=25, pady=(10, 10))
    ctk.CTkLabel(result_frame, text="Résultat", font=("Arial", 14, "bold")).pack(pady=(10, 5))
    text_result = ctk.CTkTextbox(result_frame, corner_radius=8, wrap="word", font=("Consolas", 13))
    text_result.pack(expand=True, fill="both", padx=10, pady=(0, 10))