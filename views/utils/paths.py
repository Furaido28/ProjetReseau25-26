from pathlib import Path
import sys, shutil

def resource_path(rel: str) -> Path:
    """Chemin compatible source + exe (_MEIPASS)."""
    try:
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    except Exception:
        # on remonte depuis views/utils jusqu'à la racine du projet
        base = Path(__file__).resolve().parents[2]
    return (base / rel).resolve()

def user_db_path() -> Path:
    app_dir = Path.home() / "AppData" / "Local" / "ProjetReseau"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir / "projetReseau.db"

def ensure_db_initialized() -> Path:
    """Copie la BDD seed (embarquée) vers un dossier utilisateur en écriture."""
    dst = user_db_path()
    if not dst.exists():
        seed = resource_path("bdd/projetReseau.db")  # vient du bundle (--add-data)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(seed, dst)
    return dst