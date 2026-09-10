APP_TITLE = "TSP Ho Chi Minh City Route Optimizer"

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850
WINDOW_SIZE = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"

MAP_WIDTH = 850
MAP_HEIGHT = 700

MARKER_SIZE = 12
ROUTE_LINE_WIDTH = 4

DEFAULT_THEME = "dark"

LIGHT_THEME = {
    "background": "#F8FAFC",
    "surface": "#FFFFFF",
    "sidebar": "#E2E8F0",
    "text": "#1E293B",
    "border": "#CBD5E1"
}

DARK_THEME = {
    "background": "#0F172A",
    "surface": "#1E293B",
    "sidebar": "#172554",
    "text": "#F8FAFC",
    "border": "#334155"
}

ALGORITHM_COLORS = {
    "Brute Force": "#EF4444",
    "Greedy": "#22C55E",
    "GBFS": "#2563EB"
}

FONT_FAMILY = "Segoe UI"

TITLE_FONT = (FONT_FAMILY, 24, "bold")
SUBTITLE_FONT = (FONT_FAMILY, 18, "bold")
TEXT_FONT = (FONT_FAMILY, 14)
BUTTON_FONT = (FONT_FAMILY, 14, "bold")
SMALL_FONT = (FONT_FAMILY, 12)

ANIMATION_SPEED = {
    "Slow": 700,
    "Normal": 400,
    "Fast": 150
}

DEFAULT_ANIMATION = "Normal"

CARD_WIDTH = 220
CARD_HEIGHT = 90

OUTPUT_FOLDER = "outputs"
ROUTE_FOLDER = "outputs/routes"
REPORT_FOLDER = "outputs/reports"

BUTTONS = {
    "run": "Run Algorithm",
    "compare": "Compare Algorithms",
    "reset": "Reset",
    "export": "Export Result"
}