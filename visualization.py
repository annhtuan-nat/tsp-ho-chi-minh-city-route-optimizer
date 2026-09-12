import tkintermapview
from PIL import Image, ImageDraw, ImageTk


class MapVisualizer:
    def __init__(self, parent):
        self.map_widget = tkintermapview.TkinterMapView(
            parent,
            corner_radius=0
        )

        self.map_widget.set_tile_server(
            "https://mt1.google.com/vt/lyrs=m&hl=vi&x={x}&y={y}&z={z}&s=Ga",
            max_zoom=17
        )

        self.map_widget.set_position(
            10.7769,
            106.7009
        )

        self.map_widget.set_zoom(12)

        self.cities = []
        self.markers = []
        self.current_path = None
        self.start_city_id = 0
        self.on_map_click_callback = None

        self.city_icon = self.create_pin_icon(
            "#1976D2"
        )

        self.start_icon = self.create_pin_icon(
            "#F9A825"
        )

        self.map_widget.add_left_click_map_command(
            self.handle_map_click
        )

    def create_pin_icon(self, color):
        width = 40
        height = 48

        image = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(image)

        draw.ellipse(
            (4, 2, 36, 34),
            fill="#111111"
        )

        draw.polygon(
            [
                (8, 26),
                (20, 46),
                (32, 26)
            ],
            fill="#111111"
        )

        draw.ellipse(
            (7, 5, 33, 31),
            fill=color
        )

        draw.polygon(
            [
                (11, 25),
                (20, 42),
                (29, 25)
            ],
            fill=color
        )

        draw.ellipse(
            (13, 11, 27, 25),
            fill="#FFFFFF"
        )

        return ImageTk.PhotoImage(image)

    def pack(self, **kwargs):
        self.map_widget.pack(**kwargs)

    def grid(self, **kwargs):
        self.map_widget.grid(**kwargs)

    def place(self, **kwargs):
        self.map_widget.place(**kwargs)

    def set_click_callback(self, callback):
        self.on_map_click_callback = callback

    def handle_map_click(self, coordinates):
        latitude, longitude = coordinates

        if self.on_map_click_callback:
            self.on_map_click_callback(
                latitude,
                longitude
            )

    def set_cities(self, cities):
        self.cities = list(cities)
        self.redraw_markers()

    def set_start_city(self, city_id):
        self.start_city_id = (
            0 if city_id is None else city_id
        )

        self.redraw_markers()

    def redraw_markers(self):
        self.clear_markers()

        for city in self.cities:
            if city.id == self.start_city_id:
                icon = self.start_icon
            else:
                icon = self.city_icon

            marker = self.map_widget.set_marker(
                city.latitude,
                city.longitude,
                text=f"P{city.id + 1}",
                icon=icon,
                icon_anchor="center",
                font=("Segoe UI", 12, "bold"),
                text_color="#111111"
            )

            self.markers.append(
                marker
            )

    def set_route(self, route):
        self.current_path = list(route)

        self.clear_path()

        positions = self.get_route_positions(
            route
        )

        if len(positions) < 2:
            return

        positions.append(
            positions[0]
        )

        self.map_widget.set_path(
            positions,
            color="#FFFFFF",
            width=11
        )

        self.map_widget.set_path(
            positions,
            color="#7B1FA2",
            width=6
        )

    def animate_route(
        self,
        route,
        delay=220
    ):
        self.clear_path()

        positions = self.get_route_positions(
            route
        )

        if len(positions) < 2:
            return

        positions.append(
            positions[0]
        )

        self.current_path = list(route)

        self.animate_step(
            positions,
            1,
            positions[:1],
            delay
        )

    def animate_step(
        self,
        positions,
        index,
        visible_positions,
        delay
    ):
        if index >= len(positions):
            self.set_route(
                self.current_path
            )
            return

        visible_positions.append(
            positions[index]
        )

        self.clear_path()

        if len(visible_positions) >= 2:
            self.map_widget.set_path(
                visible_positions,
                color="#FFFFFF",
                width=11
            )

            self.map_widget.set_path(
                visible_positions,
                color="#7B1FA2",
                width=6
            )

        self.map_widget.after(
            delay,
            lambda: self.animate_step(
                positions,
                index + 1,
                visible_positions,
                delay
            )
        )

    def get_route_positions(self, route):
        positions = []

        for city_id in route:
            city = self.get_city(
                city_id
            )

            if city is not None:
                positions.append(
                    (
                        city.latitude,
                        city.longitude
                    )
                )

        return positions

    def clear_markers(self):
        self.map_widget.delete_all_marker()
        self.markers = []

    def clear_path(self):
        self.map_widget.delete_all_path()

    def clear(self):
        self.cities = []
        self.markers = []
        self.current_path = None
        self.start_city_id = 0

        self.clear_markers()
        self.clear_path()

        self.map_widget.set_position(
            10.7769,
            106.7009
        )

        self.map_widget.set_zoom(12)

    def get_city(self, city_id):
        for city in self.cities:
            if 0 <= city_id < len(self.cities):
                return self.cities[city_id]
            return None

    def get_city_count(self):
        return len(self.cities)

    def focus_hcm(self):
        self.map_widget.set_position(
            10.7769,
            106.7009
        )

        self.map_widget.set_zoom(12)