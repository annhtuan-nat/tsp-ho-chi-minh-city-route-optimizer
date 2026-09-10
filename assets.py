from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"

LOGO = ASSETS_DIR / "logo.png"
MAP = ASSETS_DIR / "hcm_map.png"

ICONS = {
    "run": ICONS_DIR / "run.png",
    "reset": ICONS_DIR / "reset.png",
    "compare": ICONS_DIR / "compare.png",
    "export": ICONS_DIR / "export.png",
    "location": ICONS_DIR / "location.png",
    "theme": ICONS_DIR / "theme.png"
}


def get_logo():
    return str(LOGO)


def get_map():
    return str(MAP)


def get_icon(name):
    icon = ICONS.get(name)
    if icon and icon.exists():
        return str(icon)
    return None


def asset_exists(path):
    return Path(path).exists()


def create_output_folders():
    (BASE_DIR / "outputs").mkdir(exist_ok=True)
    (BASE_DIR / "outputs" / "routes").mkdir(exist_ok=True)
    (BASE_DIR / "outputs" / "reports").mkdir(exist_ok=True)
    (BASE_DIR / "outputs" / "charts").mkdir(exist_ok=True)