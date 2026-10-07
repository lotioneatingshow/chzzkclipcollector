import json
from pathlib import Path

import tkinter as tk


SETTINGS_FILENAME = "settings.json"

DEFAULT_SETTINGS = {
    "theme": "light",
}


def get_settings_file(
    base_directory: Path,
):
    """
    exe 또는 메인 스크립트 위치 하위의 config 폴더 내에
    settings.json 경로를 반환하며, config 폴더가 없으면 자동 생성합니다.
    """
    config_directory = (
        base_directory / "config"
    )

    config_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return (
        config_directory
        / SETTINGS_FILENAME
    )


def load_settings(
    base_directory: Path,
):
    settings_file = get_settings_file(
        base_directory
    )

    if not settings_file.exists():
        return dict(
            DEFAULT_SETTINGS
        )

    try:
        with open(
            settings_file,
            "r",
            encoding="utf-8",
        ) as file:
            settings = json.load(
                file
            )

        if not isinstance(
            settings,
            dict,
        ):
            return dict(
                DEFAULT_SETTINGS
            )

        result = dict(
            DEFAULT_SETTINGS
        )

        result.update(
            settings
        )

        if result["theme"] not in {
            "light",
            "dark",
        }:
            result["theme"] = "light"

        return result

    except (
        OSError,
        ValueError,
        json.JSONDecodeError,
    ):
        return dict(
            DEFAULT_SETTINGS
        )


def save_settings(
    base_directory: Path,
    settings,
):
    settings_file = get_settings_file(
        base_directory
    )

    try:
        with open(
            settings_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                settings,
                file,
                ensure_ascii=False,
                indent=4,
            )

        return True

    except OSError:
        return False


class SettingsWindow:
    def __init__(
        self,
        app,
    ):
        self.app = app

        self.window = tk.Toplevel(
            app.root
        )

        self.window.title(
            "설정"
        )

        self.window.geometry(
            "360x230"
        )

        self.window.resizable(
            False,
            False,
        )

        self.window.transient(
            app.root
        )

        self.window.grab_set()

        self.center_window()

        self.build_ui()

        self.apply_theme()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close,
        )

    def center_window(self):
        self.window.update_idletasks()

        width = 360
        height = 230

        screen_width = (
            self.window.winfo_screenwidth()
        )

        screen_height = (
            self.window.winfo_screenheight()
        )

        x = (
            screen_width - width
        ) // 2

        y = (
            screen_height - height
        ) // 2

        self.window.geometry(
            f"{width}x{height}+{x}+{y}"
        )

        self.window.lift()

        try:
            self.window.attributes(
                "-topmost",
                True,
            )

            self.window.after(
                200,
                lambda: self.window.attributes(
                    "-topmost",
                    False,
                ),
            )

        except tk.TclError:
            pass

        self.window.focus_force()

    def build_ui(self):
        title = tk.Label(
            self.window,
            text="설정",
            font=(
                "맑은 고딕",
                16,
                "bold",
            ),
        )

        title.pack(
            pady=(20, 15),
        )

        theme_label = tk.Label(
            self.window,
            text="테마",
            font=(
                "맑은 고딕",
                11,
                "bold",
            ),
            anchor="w",
        )

        theme_label.pack(
            fill="x",
            padx=35,
        )

        self.theme_var = tk.StringVar(
            value=self.app.theme_name
        )

        theme_frame = tk.Frame(
            self.window
        )

        theme_frame.pack(
            fill="x",
            padx=35,
            pady=(8, 20),
        )

        tk.Radiobutton(
            theme_frame,
            text="화이트",
            value="light",
            variable=self.theme_var,
            command=self.change_theme,
            font=(
                "맑은 고딕",
                10,
            ),
        ).pack(
            side="left",
        )

        tk.Radiobutton(
            theme_frame,
            text="다크",
            value="dark",
            variable=self.theme_var,
            command=self.change_theme,
            font=(
                "맑은 고딕",
                10,
            ),
        ).pack(
            side="left",
            padx=(30, 0),
        )

        tk.Button(
            self.window,
            text="닫기",
            font=(
                "맑은 고딕",
                10,
            ),
            width=12,
            command=self.close,
        ).pack()

    def change_theme(self):
        theme_name = self.theme_var.get()

        self.app.set_theme(
            theme_name
        )

        self.apply_theme()

    def apply_theme(self):
        from .theme import (
            configure_widget_theme,
            get_theme,
        )

        theme = get_theme(
            self.app.theme_name
        )

        configure_widget_theme(
            self.window,
            theme,
        )

    def close(self):
        try:
            self.window.grab_release()
        except tk.TclError:
            pass

        self.window.destroy()