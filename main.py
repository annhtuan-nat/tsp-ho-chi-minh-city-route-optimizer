import customtkinter as ctk

from gui import TSPApplication
from assets import create_output_folders


def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    create_output_folders()

    app = TSPApplication()
    app.mainloop()


if __name__ == "__main__":
    main()