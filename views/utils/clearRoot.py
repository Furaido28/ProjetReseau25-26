def clear_root(root):
    """Efface tout le contenu de la fenêtre."""
    for widget in root.winfo_children():
        widget.destroy()