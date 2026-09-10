from pathlib import Path
import customtkinter as ctk
from PIL import Image

from settings import *
from assets import get_logo, get_map
from city_data import get_city_names

ctk.set_appearance_mode(DEFAULT_THEME)
ctk.set_default_color_theme("blue")


class TSPApplication(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)

        self.algorithm = ctk.StringVar(value="Brute Force")
        self.start_city = ctk.StringVar(value=get_city_names()[0])
        self.animation_speed = ctk.StringVar(value=DEFAULT_ANIMATION)

        self.create_layout()

    def create_layout(self):
        self.header_frame = ctk.CTkFrame(self, height=70, corner_radius=0)
        self.header_frame.pack(fill="x")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        self.sidebar_frame = ctk.CTkFrame(self.content_frame, width=250)
        self.sidebar_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        self.map_frame = ctk.CTkFrame(self.content_frame)
        self.map_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        self.dashboard_frame = ctk.CTkFrame(self.content_frame, width=250)
        self.dashboard_frame.pack(side="right", fill="y", padx=(5, 10), pady=10)

        self.timeline_frame = ctk.CTkFrame(self, height=110)
        self.timeline_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.create_header()
        self.create_sidebar()
        self.create_map()
        self.create_dashboard()
        self.create_timeline()

    def create_header(self):
        logo_path = get_logo()

        if logo_path and Path(logo_path).exists():
            logo = ctk.CTkImage(Image.open(logo_path), size=(45, 45))

            ctk.CTkLabel(
                self.header_frame,
                image=logo,
                text=""
            ).pack(side="left", padx=15, pady=10)

        ctk.CTkLabel(
            self.header_frame,
            text="TSP Ho Chi Minh City Route Optimizer",
            font=TITLE_FONT
        ).pack(side="left")

        self.theme_button = ctk.CTkButton(
            self.header_frame,
            text="Dark / Light",
            width=120,
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right", padx=20)

    def create_sidebar(self):
        ctk.CTkLabel(
            self.sidebar_frame,
            text="Algorithm",
            font=SUBTITLE_FONT
        ).pack(anchor="w", padx=15, pady=(20, 5))

        ctk.CTkComboBox(
            self.sidebar_frame,
            values=["Brute Force", "Greedy", "GBFS"],
            variable=self.algorithm,
            width=220
        ).pack(padx=15)

        ctk.CTkLabel(
            self.sidebar_frame,
            text="Start Location",
            font=SUBTITLE_FONT
        ).pack(anchor="w", padx=15, pady=(20, 5))

        ctk.CTkComboBox(
            self.sidebar_frame,
            values=get_city_names(),
            variable=self.start_city,
            width=220
        ).pack(padx=15)

        ctk.CTkLabel(
            self.sidebar_frame,
            text="Animation Speed",
            font=SUBTITLE_FONT
        ).pack(anchor="w", padx=15, pady=(20, 5))

        ctk.CTkComboBox(
            self.sidebar_frame,
            values=["Slow", "Normal", "Fast"],
            variable=self.animation_speed,
            width=220
        ).pack(padx=15)

        self.run_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Run Algorithm",
            width=220
        )
        self.run_button.pack(padx=15, pady=(25, 10))

        self.compare_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Compare Algorithms",
            width=220
        )
        self.compare_button.pack(padx=15, pady=10)

        self.reset_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Reset",
            width=220
        )
        self.reset_button.pack(padx=15, pady=10)

        self.export_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Export Result",
            width=220
        )
        self.export_button.pack(padx=15, pady=10)

    def create_map(self):
        map_path = get_map()

        if map_path and Path(map_path).exists():
            map_image = ctk.CTkImage(
                Image.open(map_path),
                size=(MAP_WIDTH, MAP_HEIGHT)
            )

            self.map_label = ctk.CTkLabel(
                self.map_frame,
                image=map_image,
                text=""
            )
        else:
            self.map_label = ctk.CTkLabel(
                self.map_frame,
                text="HO CHI MINH CITY MAP\n\nPlease add hcm_map.png to assets folder",
                width=MAP_WIDTH,
                height=MAP_HEIGHT,
                fg_color="#D1D5DB",
                text_color="black",
                font=SUBTITLE_FONT,
                corner_radius=15
            )

        self.map_label.pack(padx=10, pady=10)

    def create_dashboard(self):
        ctk.CTkLabel(
            self.dashboard_frame,
            text="Dashboard",
            font=SUBTITLE_FONT
        ).pack(pady=20)

        self.algorithm_card = self.create_card(
            "Algorithm",
            "Waiting..."
        )

        self.distance_card = self.create_card(
            "Total Distance",
            "0 km"
        )

        self.time_card = self.create_card(
            "Execution Time",
            "0 s"
        )

        self.city_card = self.create_card(
            "Visited Cities",
            "0"
        )

    def create_card(self, title, value):
        frame = ctk.CTkFrame(
            self.dashboard_frame,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            corner_radius=15
        )
        frame.pack(pady=10, padx=10)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 13, "bold")
        ).pack(pady=(12, 2))

        label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Segoe UI", 16, "bold")
        )
        label.pack()

        return label

    def create_timeline(self):
        ctk.CTkLabel(
            self.timeline_frame,
            text="Route Timeline",
            font=SUBTITLE_FONT
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.timeline_text = ctk.CTkTextbox(
            self.timeline_frame,
            height=55
        )
        self.timeline_text.pack(fill="x", padx=20, pady=(0, 10))
        self.timeline_text.insert("1.0", "Waiting for route...")
        self.timeline_text.configure(state="disabled")

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")