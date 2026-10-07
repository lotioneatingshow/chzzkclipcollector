import tkinter as tk
from tkinter import font


MAIN_TITLE_FONT = (
    "맑은 고딕",
    20,
    "bold",
)


THEMES = {
    "light": {
        "bg": "#F5F5F5",
        "surface": "#FFFFFF",
        "input": "#FFFFFF",
        "text": "#202020",
        "muted": "#707070",
        "border": "#CFCFCF",
        "accent": "#168F5C",
        "accent_active": "#12754B",
        "accent_text": "#FFFFFF",
        "title_text": "#168F5C",
        "neutral_bg": "#D6D6D6",
        "neutral_active": "#BEBEBE",
        "neutral_text": "#202020",
        "disabled_bg": "#D8D8D8",
        "disabled_text": "#8A8A8A",
        "log_bg": "#FFFFFF",
    },
    "dark": {
        "bg": "#111111",
        "surface": "#1B1B1B",
        "input": "#181818",
        "text": "#F2F2F2",
        "muted": "#A0A0A0",
        "border": "#444444",
        "accent": "#00E693",
        "accent_active": "#00C77E",
        "accent_text": "#111111",
        "title_text": "#00E693",
        "neutral_bg": "#3A3A3A",
        "neutral_active": "#4A4A4A",
        "neutral_text": "#F2F2F2",
        "disabled_bg": "#2B2B2B",
        "disabled_text": "#777777",
        "log_bg": "#181818",
    },
}


NEUTRAL_BUTTON_TEXTS = {
    "닫기",
    "전체 선택",
    "전체 해제",
    "이전",
    "다음",
}


def get_theme(theme_name):
    if theme_name not in THEMES:
        theme_name = "light"

    return dict(THEMES[theme_name])


def configure_widget_theme(widget, theme):
    _configure_widget(widget, theme)


def _configure_widget(widget, theme):
    try:
        if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
            widget.configure(
                background=theme["bg"]
            )

        elif isinstance(widget, tk.Button):
            state = str(widget.cget("state"))
            text = str(widget.cget("text")).strip()

            is_neutral = (
                text in NEUTRAL_BUTTON_TEXTS
            )

            if is_neutral:
                background = theme["neutral_bg"]
                foreground = theme["neutral_text"]
                active_background = theme["neutral_active"]
                active_foreground = theme["neutral_text"]
                relief = "solid"
                borderwidth = 1
            else:
                background = theme["accent"]
                foreground = theme["accent_text"]
                active_background = theme["accent_active"]
                active_foreground = theme["accent_text"]
                relief = "flat"
                borderwidth = 0

            if state == "disabled":
                background = theme["disabled_bg"]
                foreground = theme["disabled_text"]
                active_background = theme["disabled_bg"]
                active_foreground = theme["disabled_text"]

            widget.configure(
                background=background,
                foreground=foreground,
                activebackground=active_background,
                activeforeground=active_foreground,
                disabledforeground=theme["disabled_text"],
                relief=relief,
                borderwidth=borderwidth,
                highlightthickness=0,
            )

            try:
                current_font = widget.cget("font")

                if current_font:
                    font_obj = font.Font(
                        font=current_font
                    )
                    widget.configure(
                        font=(
                            font_obj.actual("family"),
                            font_obj.actual("size"),
                            "bold",
                        )
                    )

            except (tk.TclError, tk.TclError):
                pass

        elif isinstance(widget, tk.Radiobutton):
            widget.configure(
                background=theme["surface"],
                foreground=theme["text"],
                activebackground=theme["surface"],
                activeforeground=theme["text"],
                selectcolor=theme["surface"],
                disabledforeground=theme["disabled_text"],
            )

        elif isinstance(widget, tk.Checkbutton):
            widget.configure(
                background=theme["surface"],
                foreground=theme["text"],
                activebackground=theme["surface"],
                activeforeground=theme["text"],
                selectcolor=theme["surface"],
                disabledforeground=theme["disabled_text"],
            )

        elif isinstance(widget, tk.Entry):
            widget.configure(
                background=theme["input"],
                foreground=theme["text"],
                insertbackground=theme["text"],
                disabledforeground=theme["disabled_text"],
                highlightbackground=theme["border"],
                highlightcolor=theme["accent"],
            )

        elif isinstance(widget, tk.Text):
            widget.configure(
                background=theme["log_bg"],
                foreground=theme["text"],
                insertbackground=theme["text"],
                highlightbackground=theme["border"],
                highlightcolor=theme["accent"],
            )

        elif isinstance(widget, tk.Canvas):
            widget.configure(
                background=theme["surface"],
                highlightbackground=theme["border"],
            )

        elif isinstance(widget, tk.Scrollbar):
            widget.configure(
                background=theme["surface"],
                troughcolor=theme["bg"],
                activebackground=theme["neutral_active"],
                highlightbackground=theme["border"],
            )

        elif isinstance(widget, tk.Label):
            widget.configure(
                background=theme["bg"],
                foreground=theme["text"],
            )

        elif isinstance(widget, tk.Frame):
            widget.configure(
                background=theme["bg"]
            )

            try:
                if widget.cget("relief") != "flat":
                    widget.configure(
                        highlightbackground=theme["border"]
                    )
            except tk.TclError:
                pass

    except tk.TclError:
        pass

    try:
        for child in widget.winfo_children():
            _configure_widget(child, theme)
    except tk.TclError:
        pass