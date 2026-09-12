import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import random

from city_data import CityManager
from graph import build_distance_matrix
from algorithms import run_algorithm
from visualization import MapVisualizer


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


BG = "#07111D"
SIDEBAR = "#0C1828"
CARD = "#13243A"
CARD_2 = "#182C46"
BORDER = "#27415F"

TEXT = "#F4F7FA"
MUTED = "#93A6BB"

ORANGE = "#F2A900"
ORANGE_HOVER = "#FFBC3A"

CYAN = "#00C7B7"
GREEN = "#4ADE80"
RED = "#FF5F56"

ALGORITHMS = [
    "Vét cạn",
    "Quy hoạch động",
    "Heuristic"
]


def format_time(seconds):
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} µs"

    if seconds < 1:
        return f"{seconds * 1000:.2f} ms"

    return f"{seconds:.3f} s"


def compare_results(results):
    if not results:
        return []

    optimal_distance = min(
        result["distance"]
        for result in results
    )

    comparison = []

    for result in results:
        difference = 0.0

        if optimal_distance > 0:
            difference = (
                (result["distance"] - optimal_distance)
                / optimal_distance
            ) * 100

        comparison.append({
            "algorithm": result["algorithm"],
            "distance": result["distance"],
            "execution_time": result["execution_time"],
            "number_of_points": result["number_of_points"],
            "difference_percent": difference
        })

    return comparison


class TSPApplication:
    def __init__(self, root):
        self.root = root

        self.root.title(
            "TSP Route Optimizer - TP. Hồ Chí Minh"
        )

        self.root.geometry(
            "1650x930"
        )

        self.root.minsize(
            1350,
            780
        )

        self.root.configure(
            bg=BG
        )

        self.city_manager = CityManager()

        self.results = []
        self.current_result = None
        self.edit_mode = False
        self.current_panel = "result"

        self.build_ui()

    def build_ui(self):
        self.build_header()

        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=BG,
            corner_radius=0
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 15)
        )

        self.build_sidebar()
        self.build_map()
        self.build_result_panel()

    def build_header(self):
        header = ctk.CTkFrame(
            self.root,
            fg_color=BG,
            height=72,
            corner_radius=0
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(12, 5)
        )

        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            title_frame,
            text="TSP",
            text_color=ORANGE,
            font=("Segoe UI", 32, "bold")
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            title_frame,
            text=" ROUTE OPTIMIZER",
            text_color=TEXT,
            font=("Segoe UI", 32, "bold")
        ).pack(
            side="left",
            padx=(3, 0)
        )

        ctk.CTkLabel(
            header,
            text="Bài toán Người du lịch • TP. HỒ CHÍ MINH",
            text_color=MUTED,
            font=("Segoe UI", 11)
        ).pack(
            side="left",
            padx=25
        )

        self.status_label = ctk.CTkLabel(
            header,
            text="● Sẵn sàng",
            text_color=GREEN,
            font=("Segoe UI", 11, "bold")
        )

        self.status_label.pack(
            side="right"
        )

    def build_sidebar(self):
        sidebar = ctk.CTkFrame(
            self.main_frame,
            width=250,
            fg_color=SIDEBAR,
            corner_radius=12
        )

        sidebar.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="ĐIỀU KHIỂN",
            text_color=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(22, 22)
        )

        self.section_label(
            sidebar,
            "ĐIỂM BẮT ĐẦU"
        )

        self.start_var = ctk.StringVar(
            value=""
        )

        self.start_combo = ctk.CTkComboBox(
            sidebar,
            variable=self.start_var,
            values=[],
            state="readonly",
            height=40,
            fg_color=CARD,
            border_color=BORDER,
            button_color=CARD_2,
            button_hover_color=BORDER,
            text_color=TEXT,
            font=("Segoe UI", 11)
        )

        self.start_combo.pack(
            fill="x",
            padx=20,
            pady=(6, 18)
        )

        self.start_combo.bind(
            "<<ComboboxSelected>>",
            self.change_start
        )

        self.section_label(
            sidebar,
            "THUẬT TOÁN"
        )

        self.algorithm_var = ctk.StringVar(
            value="Vét cạn"
        )

        self.algorithm_combo = ctk.CTkComboBox(
            sidebar,
            variable=self.algorithm_var,
            values=ALGORITHMS,
            state="readonly",
            height=40,
            fg_color=CARD,
            border_color=BORDER,
            button_color=CARD_2,
            button_hover_color=BORDER,
            text_color=TEXT,
            font=("Segoe UI", 11)
        )

        self.algorithm_combo.pack(
            fill="x",
            padx=20,
            pady=(6, 18)
        )

        self.section_label(
            sidebar,
            "TỐC ĐỘ MÔ PHỎNG"
        )

        self.speed_var = ctk.StringVar(
            value="Bình thường"
        )

        self.speed_combo = ctk.CTkComboBox(
            sidebar,
            variable=self.speed_var,
            values=[
                "Chậm",
                "Bình thường",
                "Nhanh"
            ],
            state="readonly",
            height=40,
            fg_color=CARD,
            border_color=BORDER,
            button_color=CARD_2,
            button_hover_color=BORDER,
            text_color=TEXT,
            font=("Segoe UI", 11)
        )

        self.speed_combo.pack(
            fill="x",
            padx=20,
            pady=(6, 20)
        )

        self.edit_button = self.make_button(
            sidebar,
            "＋  Thêm / Xóa điểm",
            self.toggle_edit_mode
        )

        self.make_button(
            sidebar,
            "✦  Tạo điểm ngẫu nhiên",
            self.random_points
        )

        self.make_button(
            sidebar,
            "▶  GIẢI TSP",
            self.solve_tsp,
            primary=True
        )

        self.make_button(
            sidebar,
            "⇄  So sánh 3 thuật toán",
            self.compare_algorithms
        )

        self.make_button(
            sidebar,
            "⌫  Xóa bản đồ",
            self.clear_map
        )

        self.make_button(
            sidebar,
            "↻  Đặt lại kết quả",
            self.reset_result
        )

        tk.Frame(
            sidebar,
            bg=SIDEBAR
        ).pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            sidebar,
            text="Bật Thêm / Xóa điểm rồi click trên bản đồ.",
            text_color=MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

    def section_label(
        self,
        parent,
        text
    ):
        ctk.CTkLabel(
            parent,
            text=text,
            text_color=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w",
            padx=20
        )

    def make_button(
        self,
        parent,
        text,
        command,
        primary=False
    ):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=43,
            corner_radius=8,
            fg_color=(
                ORANGE
                if primary
                else CARD
            ),
            hover_color=(
                ORANGE_HOVER
                if primary
                else CARD_2
            ),
            text_color=(
                BG
                if primary
                else TEXT
            ),
            font=("Segoe UI", 10, "bold")
        )

        button.pack(
            fill="x",
            padx=20,
            pady=4
        )

        return button

    def build_map(self):
        center = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG,
            corner_radius=0
        )

        center.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        top = ctk.CTkFrame(
            center,
            fg_color="transparent",
            height=48
        )

        top.pack(
            fill="x"
        )

        top.pack_propagate(False)

        ctk.CTkLabel(
            top,
            text="BẢN ĐỒ TP. HỒ CHÍ MINH",
            text_color=TEXT,
            font=("Segoe UI", 17, "bold")
        ).pack(
            side="left"
        )

        self.point_count_label = ctk.CTkLabel(
            top,
            text="0 điểm",
            text_color=MUTED,
            font=("Segoe UI", 10)
        )

        self.point_count_label.pack(
            side="right"
        )

        map_frame = ctk.CTkFrame(
            center,
            fg_color=BORDER,
            corner_radius=11
        )

        map_frame.pack(
            fill="both",
            expand=True
        )

        self.visualizer = MapVisualizer(
            map_frame
        )

        self.visualizer.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1
        )

        self.visualizer.set_click_callback(
            self.map_clicked
        )

    def build_result_panel(self):
        right = ctk.CTkFrame(
            self.main_frame,
            width=440,
            fg_color=SIDEBAR,
            corner_radius=12
        )

        right.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        right.pack_propagate(False)

        tab_frame = ctk.CTkFrame(
            right,
            fg_color="transparent",
            height=50
        )

        tab_frame.pack(
            fill="x",
            padx=12,
            pady=(10, 0)
        )

        tab_frame.pack_propagate(False)

        self.result_tab = ctk.CTkButton(
            tab_frame,
            text="KẾT QUẢ",
            command=self.show_result_panel,
            height=37,
            corner_radius=7,
            fg_color=ORANGE,
            hover_color=ORANGE_HOVER,
            text_color=BG,
            font=("Segoe UI", 10, "bold")
        )

        self.result_tab.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 4),
            pady=5
        )

        self.detail_tab = ctk.CTkButton(
            tab_frame,
            text="CHI TIẾT LỘ TRÌNH",
            command=self.show_detail_panel,
            height=37,
            corner_radius=7,
            fg_color=CARD,
            hover_color=CARD_2,
            text_color=TEXT,
            font=("Segoe UI", 10, "bold")
        )

        self.detail_tab.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 0),
            pady=5
        )

        self.result_container = ctk.CTkFrame(
            right,
            fg_color="transparent"
        )

        self.result_container.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(5, 12)
        )

        self.build_result_view()
        self.build_detail_view()

        self.show_result_panel()

    def build_result_view(self):
        self.result_view = ctk.CTkFrame(
            self.result_container,
            fg_color="transparent"
        )

        self.result_view.pack(
            fill="both",
            expand=True
        )

        overview = ctk.CTkFrame(
            self.result_view,
            fg_color="transparent"
        )

        overview.pack(
            fill="x",
            padx=3
        )

        overview.grid_columnconfigure(
            0,
            weight=1,
            uniform="metric"
        )

        overview.grid_columnconfigure(
            1,
            weight=1,
            uniform="metric"
        )

        self.algorithm_value = self.grid_metric(
            overview,
            "THUẬT TOÁN",
            "-",
            0,
            0
        )

        self.distance_value = self.grid_metric(
            overview,
            "KHOẢNG CÁCH",
            "-",
            0,
            1
        )

        self.time_value = self.grid_metric(
            overview,
            "THỜI GIAN",
            "-",
            1,
            0
        )

        self.points_value = self.grid_metric(
            overview,
            "SỐ ĐIỂM",
            "0",
            1,
            1
        )

        complexity_box = ctk.CTkFrame(
            self.result_view,
            fg_color=CARD,
            corner_radius=8,
            height=52
        )

        complexity_box.pack(
            fill="x",
            padx=3,
            pady=4
        )

        complexity_box.pack_propagate(False)

        ctk.CTkLabel(
            complexity_box,
            text="ĐỘ PHỨC TẠP",
            text_color=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            side="left",
            padx=12
        )

        self.complexity_value = ctk.CTkLabel(
            complexity_box,
            text="-",
            text_color=TEXT,
            font=("Segoe UI", 11, "bold")
        )

        self.complexity_value.pack(
            side="right",
            padx=12
        )

        route_box = ctk.CTkFrame(
            self.result_view,
            fg_color=CARD,
            corner_radius=8,
            height=82
        )

        route_box.pack(
            fill="x",
            padx=3,
            pady=4
        )

        route_box.pack_propagate(False)

        ctk.CTkLabel(
            route_box,
            text="LỘ TRÌNH TSP",
            text_color=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=11,
            pady=(8, 2)
        )

        self.route_label = ctk.CTkLabel(
            route_box,
            text="-",
            text_color=CYAN,
            anchor="w",
            justify="left",
            wraplength=395,
            font=("Segoe UI", 10, "bold")
        )

        self.route_label.pack(
            anchor="w",
            padx=11
        )

        comparison_box = ctk.CTkFrame(
            self.result_view,
            fg_color=CARD,
            corner_radius=8
        )

        comparison_box.pack(
            fill="both",
            expand=True,
            padx=3,
            pady=(4, 3)
        )

        ctk.CTkLabel(
            comparison_box,
            text="SO SÁNH 3 THUẬT TOÁN",
            text_color=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(11, 9)
        )

        table_header = ctk.CTkFrame(
            comparison_box,
            fg_color=CARD_2,
            corner_radius=6,
            height=34
        )

        table_header.pack(
            fill="x",
            padx=9
        )

        table_header.pack_propagate(False)

        ctk.CTkLabel(
            table_header,
            text="THUẬT TOÁN",
            text_color=MUTED,
            anchor="w",
            font=("Segoe UI", 8, "bold")
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=9
        )

        ctk.CTkLabel(
            table_header,
            text="KHOẢNG CÁCH",
            text_color=MUTED,
            width=100,
            font=("Segoe UI", 8, "bold")
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            table_header,
            text="THỜI GIAN",
            text_color=MUTED,
            width=90,
            font=("Segoe UI", 8, "bold")
        ).pack(
            side="left"
        )

        self.compare_area = ctk.CTkFrame(
            comparison_box,
            fg_color=CARD
        )

        self.compare_area.pack(
            fill="both",
            expand=True,
            padx=9,
            pady=7
        )

    def grid_metric(
        self,
        parent,
        title,
        value,
        row,
        column
    ):
        box = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=8,
            height=66
        )

        box.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=3,
            pady=3
        )

        box.grid_propagate(False)

        ctk.CTkLabel(
            box,
            text=title,
            text_color=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(8, 0)
        )

        label = ctk.CTkLabel(
            box,
            text=value,
            text_color=TEXT,
            anchor="w",
            font=("Segoe UI", 12, "bold")
        )

        label.pack(
            anchor="w",
            padx=10,
            pady=(2, 0)
        )

        return label

    def build_detail_view(self):
        self.detail_view = ctk.CTkFrame(
            self.result_container,
            fg_color="transparent"
        )

        self.detail_scroll = ctk.CTkScrollableFrame(
            self.detail_view,
            fg_color=CARD,
            corner_radius=8,
            scrollbar_button_color=CARD_2,
            scrollbar_button_hover_color=BORDER
        )

        self.detail_scroll.pack(
            fill="both",
            expand=True
        )

    def show_result_panel(self):
        self.current_panel = "result"

        self.detail_view.pack_forget()

        self.result_view.pack(
            fill="both",
            expand=True
        )

        self.result_tab.configure(
            fg_color=ORANGE,
            text_color=BG
        )

        self.detail_tab.configure(
            fg_color=CARD,
            text_color=TEXT
        )

    def show_detail_panel(self):
        self.current_panel = "detail"

        self.result_view.pack_forget()

        self.detail_view.pack(
            fill="both",
            expand=True
        )

        self.result_tab.configure(
            fg_color=CARD,
            text_color=TEXT
        )

        self.detail_tab.configure(
            fg_color=ORANGE,
            text_color=BG
        )

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

        if self.edit_mode:
            self.edit_button.configure(
                text="✓  Đang thêm / xóa",
                fg_color=ORANGE,
                text_color=BG
            )

            self.status_label.configure(
                text="● Click trống: thêm | Click marker: xóa",
                text_color=ORANGE
            )

        else:
            self.edit_button.configure(
                text="＋  Thêm / Xóa điểm",
                fg_color=CARD,
                text_color=TEXT
            )

            self.status_label.configure(
                text="● Sẵn sàng",
                text_color=GREEN
            )

    def map_clicked(
        self,
        latitude,
        longitude
    ):
        if not self.edit_mode:
            self.status_label.configure(
                text="● Bật Thêm / Xóa điểm trước",
                text_color=ORANGE
            )
            return

        city_id = self.find_nearby_city(
            latitude,
            longitude
        )

        if city_id is not None:
            self.remove_city(
                city_id
            )
            return

        self.city_manager.add_city(
            latitude,
            longitude,
            name="Điểm chọn trên bản đồ"
        )

        self.reset_result_only()
        self.refresh()

        self.status_label.configure(
            text="● Đã thêm điểm",
            text_color=GREEN
        )

    def find_nearby_city(
        self,
        latitude,
        longitude
    ):
        for city in self.city_manager.get_cities():
            if (
                abs(latitude - city.latitude) < 0.0025
                and
                abs(longitude - city.longitude) < 0.0025
            ):
                return city.id

        return None

    def remove_city(
        self,
        city_id
    ):
        if self.city_manager.remove_city(
            city_id
        ):
            self.reset_result_only()
            self.refresh()

            self.status_label.configure(
                text="● Đã xóa điểm",
                text_color=RED
            )

    def refresh(self):
        cities = self.city_manager.get_cities()

        self.visualizer.set_start_city(
            self.city_manager.start_city_id
        )

        self.visualizer.set_cities(
            cities
        )

        self.point_count_label.configure(
            text=f"{len(cities)} điểm"
        )

        values = [
            f"P{city.id + 1}"
            for city in cities
        ]

        self.start_combo.configure(
            values=values
        )

        start = (
            self.city_manager.get_start_city()
        )

        if start:
            self.start_var.set(
                f"P{start.id + 1}"
            )
        else:
            self.start_var.set("")

    def change_start(
        self,
        event=None
    ):
        value = self.start_var.get()

        if not value:
            return

        try:
            city_id = int(
                value[1:]
            ) - 1
        except ValueError:
            return

        if self.city_manager.set_start_city(
            city_id
        ):
            self.visualizer.set_start_city(
                city_id
            )

            self.reset_result_only()

            self.status_label.configure(
                text=f"● Điểm bắt đầu: P{city_id + 1}",
                text_color=ORANGE
            )

    def random_points(self):
        dialog = ctk.CTkToplevel(
            self.root
        )

        dialog.title(
            "Tạo điểm ngẫu nhiên"
        )

        dialog.geometry(
            "360x235"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="TẠO ĐIỂM NGẪU NHIÊN",
            text_color=TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(
            pady=(22, 12)
        )

        ctk.CTkLabel(
            dialog,
            text="Số lượng điểm (3 - 16)",
            text_color=MUTED,
            font=("Segoe UI", 10)
        ).pack()

        count_var = ctk.StringVar(
            value="8"
        )

        ctk.CTkEntry(
            dialog,
            textvariable=count_var,
            justify="center",
            height=40,
            fg_color=CARD,
            border_color=BORDER,
            font=("Segoe UI", 11)
        ).pack(
            padx=75,
            fill="x",
            pady=9
        )

        def generate():
            try:
                count = int(
                    count_var.get()
                )
            except ValueError:
                messagebox.showerror(
                    "Lỗi",
                    "Số điểm phải là số nguyên."
                )
                return

            if count < 3 or count > 16:
                messagebox.showerror(
                    "Lỗi",
                    "Số điểm phải từ 3 đến 16."
                )
                return

            self.city_manager.clear()
            self.visualizer.clear()

            centers = [
                (10.7769, 106.7009),
                (10.8231, 106.6297),
                (10.8015, 106.7147),
                (10.7887, 106.7048),
                (10.7378, 106.7229),
                (10.7756, 106.6638),
                (10.8506, 106.7714),
                (10.7873, 106.6522),
                (10.7314, 106.6981),
                (10.7552, 106.6666)
            ]

            points = []
            attempts = 0

            while (
                len(points) < count
                and attempts < 10000
            ):
                attempts += 1

                center = random.choice(
                    centers
                )

                latitude = random.uniform(
                    center[0] - 0.012,
                    center[0] + 0.012
                )

                longitude = random.uniform(
                    center[1] - 0.012,
                    center[1] + 0.012
                )

                valid = True

                for old_lat, old_lon in points:
                    distance = (
                        (latitude - old_lat) ** 2
                        + (longitude - old_lon) ** 2
                    ) ** 0.5

                    if distance < 0.008:
                        valid = False
                        break

                if valid:
                    points.append(
                        (
                            latitude,
                            longitude
                        )
                    )

            for index, (
                latitude,
                longitude
            ) in enumerate(points):
                self.city_manager.add_city(
                    latitude,
                    longitude,
                    name=f"Điểm ngẫu nhiên {index + 1}"
                )

            self.reset_result_only()
            self.refresh()

            self.status_label.configure(
                text="● Đã tạo điểm ngẫu nhiên",
                text_color=GREEN
            )

            dialog.destroy()

        ctk.CTkButton(
            dialog,
            text="TẠO ĐIỂM",
            command=generate,
            height=40,
            fg_color=ORANGE,
            hover_color=ORANGE_HOVER,
            text_color=BG,
            font=("Segoe UI", 10, "bold")
        ).pack(
            padx=75,
            fill="x",
            pady=18
        )

    def solve_tsp(self):
        cities = self.city_manager.get_cities()

        if len(cities) < 3:
            messagebox.showwarning(
                "Thiếu điểm",
                "Cần ít nhất 3 điểm."
            )
            return

        algorithm = self.algorithm_var.get()

        if (
            algorithm == "Vét cạn"
            and len(cities) > 10
        ):
            messagebox.showwarning(
                "Quá nhiều điểm",
                "Vét cạn chỉ nên chạy tối đa 10 điểm."
            )
            return

        matrix = build_distance_matrix(
            cities
        )

        start = self.city_manager.start_city_id

        self.status_label.configure(
            text="● Đang giải TSP...",
            text_color=ORANGE
        )

        self.root.update_idletasks()

        try:
            result = run_algorithm(
                algorithm,
                matrix,
                start
            )
        except Exception as error:
            messagebox.showerror(
                "Lỗi thuật toán",
                str(error)
            )

            self.status_label.configure(
                text="● Có lỗi",
                text_color=RED
            )

            return

        result["number_of_points"] = len(
            cities
        )

        self.results = [result]
        self.current_result = result

        self.show_result(
            result,
            matrix,
            cities
        )

        self.visualizer.animate_route(
            result["route"],
            self.get_delay()
        )

        self.show_result_panel()

        self.status_label.configure(
            text="● Đã hoàn thành",
            text_color=GREEN
        )

    def compare_algorithms(self):
        cities = self.city_manager.get_cities()

        if len(cities) < 3:
            messagebox.showwarning(
                "Thiếu điểm",
                "Cần ít nhất 3 điểm."
            )
            return

        if len(cities) > 16:
            messagebox.showwarning(
                "Quá nhiều điểm",
                "Tối đa 16 điểm."
            )
            return

        matrix = build_distance_matrix(
            cities
        )

        start = self.city_manager.start_city_id

        self.status_label.configure(
            text="● Đang so sánh...",
            text_color=ORANGE
        )

        self.root.update_idletasks()

        results = []

        for algorithm in ALGORITHMS:
            if (
                algorithm == "Vét cạn"
                and len(cities) > 10
            ):
                continue

            try:
                result = run_algorithm(
                    algorithm,
                    matrix,
                    start
                )

                result["number_of_points"] = len(
                    cities
                )

                results.append(
                    result
                )

            except Exception as error:
                messagebox.showerror(
                    "Lỗi thuật toán",
                    f"{algorithm}: {error}"
                )

                self.status_label.configure(
                    text="● Có lỗi",
                    text_color=RED
                )

                return

        if not results:
            return

        self.results = results

        best = min(
            results,
            key=lambda item: item["distance"]
        )

        self.current_result = best

        self.show_result(
            best,
            matrix,
            cities
        )

        comparison = compare_results(
            results
        )

        self.show_comparison(
            comparison
        )

        self.visualizer.animate_route(
            best["route"],
            self.get_delay()
        )

        self.show_result_panel()

        self.status_label.configure(
            text="● So sánh hoàn thành",
            text_color=GREEN
        )

    def show_result(
        self,
        result,
        matrix,
        cities
    ):
        self.algorithm_value.configure(
            text=result["algorithm"]
        )

        self.distance_value.configure(
            text=f"{result['distance']:.2f} km"
        )

        self.time_value.configure(
            text=format_time(
                result["execution_time"]
            )
        )

        self.points_value.configure(
            text=str(
                len(cities)
            )
        )

        self.complexity_value.configure(
            text=result[
                "processing_info"
            ].get(
                "complexity",
                "-"
            )
        )

        route = result["route"]

        if route:
            route_text = " → ".join(
                f"P{city_id + 1}"
                for city_id in route
            )

            route_text += (
                f" → P{route[0] + 1}"
            )

        else:
            route_text = "-"

        self.route_label.configure(
            text=route_text
        )

        self.show_route_details(
            route,
            matrix,
            cities
        )

    def show_route_details(
        self,
        route,
        matrix,
        cities
    ):
        for widget in (
            self.detail_scroll.winfo_children()
        ):
            widget.destroy()

        if not route:
            ctk.CTkLabel(
                self.detail_scroll,
                text="Chưa có lộ trình.",
                text_color=MUTED,
                font=("Segoe UI", 10)
            ).pack(
                pady=20
            )

            return

        for index in range(
            len(route)
        ):
            current_id = route[index]

            next_id = route[
                (index + 1) % len(route)
            ]

            current_city = cities[
                current_id
            ]

            next_city = cities[
                next_id
            ]

            distance = matrix[
                current_id
            ][
                next_id
            ]

            current_name = (
                current_city.name
                or f"P{current_id + 1}"
            )

            next_name = (
                next_city.name
                or f"P{next_id + 1}"
            )

            card = ctk.CTkFrame(
                self.detail_scroll,
                fg_color=CARD_2,
                corner_radius=7
            )

            card.pack(
                fill="x",
                pady=4
            )

            ctk.CTkLabel(
                card,
                text=f"CHẶNG {index + 1}",
                text_color=ORANGE,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w",
                padx=10,
                pady=(9, 3)
            )

            ctk.CTkLabel(
                card,
                text=f"P{current_id + 1}  →  P{next_id + 1}",
                text_color=TEXT,
                font=("Segoe UI", 10, "bold")
            ).pack(
                anchor="w",
                padx=10
            )

            ctk.CTkLabel(
                card,
                text=current_name,
                text_color=MUTED,
                anchor="w",
                wraplength=360,
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                padx=10
            )

            ctk.CTkLabel(
                card,
                text=f"↓  {distance:.2f} km",
                text_color=CYAN,
                font=("Segoe UI", 10, "bold")
            ).pack(
                anchor="w",
                padx=10,
                pady=2
            )

            ctk.CTkLabel(
                card,
                text=next_name,
                text_color=MUTED,
                anchor="w",
                wraplength=360,
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                padx=10,
                pady=(0, 9)
            )

        total_distance = sum(
            matrix[
                route[index]
            ][
                route[
                    (index + 1) % len(route)
                ]
            ]
            for index in range(len(route))
        )

        total_card = ctk.CTkFrame(
            self.detail_scroll,
            fg_color=ORANGE,
            corner_radius=8
        )

        total_card.pack(
            fill="x",
            pady=(10, 5)
        )

        ctk.CTkLabel(
            total_card,
            text=f"TỔNG QUÃNG ĐƯỜNG: {total_distance:.2f} km",
            text_color=BG,
            font=("Segoe UI", 11, "bold")
        ).pack(
            pady=11
        )

    def show_comparison(
        self,
        comparison
    ):
        self.clear_comparison()

        for index, item in enumerate(
            comparison
        ):
            row = ctk.CTkFrame(
                self.compare_area,
                fg_color=(
                    CARD_2
                    if index % 2 == 0
                    else CARD
                ),
                corner_radius=6,
                height=50
            )

            row.pack(
                fill="x",
                pady=2
            )

            row.pack_propagate(False)

            ctk.CTkLabel(
                row,
                text=item["algorithm"],
                text_color=TEXT,
                anchor="w",
                font=("Segoe UI", 9, "bold")
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=9
            )

            ctk.CTkLabel(
                row,
                text=f"{item['distance']:.2f} km",
                text_color=CYAN,
                width=100,
                font=("Segoe UI", 9, "bold")
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                row,
                text=format_time(
                    item["execution_time"]
                ),
                text_color=TEXT,
                width=90,
                font=("Segoe UI", 9)
            ).pack(
                side="left"
            )

    def clear_comparison(self):
        for widget in (
            self.compare_area.winfo_children()
        ):
            widget.destroy()

    def reset_result_only(self):
        self.current_result = None
        self.results = []

        self.algorithm_value.configure(
            text="-"
        )

        self.distance_value.configure(
            text="-"
        )

        self.time_value.configure(
            text="-"
        )

        self.points_value.configure(
            text="0"
        )

        self.complexity_value.configure(
            text="-"
        )

        self.route_label.configure(
            text="-"
        )

        self.clear_comparison()

        for widget in (
            self.detail_scroll.winfo_children()
        ):
            widget.destroy()

        self.visualizer.clear_path()

    def reset_result(self):
        self.reset_result_only()

        self.show_result_panel()

        self.status_label.configure(
            text="● Sẵn sàng",
            text_color=GREEN
        )

    def clear_map(self):
        self.city_manager.clear()

        self.visualizer.clear()

        self.reset_result_only()

        self.start_var.set("")

        self.start_combo.configure(
            values=[]
        )

        self.point_count_label.configure(
            text="0 điểm"
        )

        if self.edit_mode:
            self.toggle_edit_mode()

        self.status_label.configure(
            text="● Bản đồ đã xóa",
            text_color=MUTED
        )

    def get_delay(self):
        speed = self.speed_var.get()

        if speed == "Chậm":
            return 600

        if speed == "Nhanh":
            return 100

        return 220


if __name__ == "__main__":
    root = ctk.CTk()

    app = TSPApplication(
        root
    )

    root.mainloop()