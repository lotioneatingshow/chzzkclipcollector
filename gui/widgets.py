from pathlib import Path
import tkinter as tk


def prepare_window(
    window,
    title,
    width,
    height,
):
    window.title(title)

    icon_path = Path(__file__).resolve().parent.parent / "res" / "icon.ico"
    if icon_path.exists():
        try:
            window.iconbitmap(str(icon_path))
        except Exception:
            pass

    window.geometry(
        f"{width}x{height}"
    )

    window.resizable(
        False,
        False,
    )

    window.update_idletasks()

    screen_width = (
        window.winfo_screenwidth()
    )

    screen_height = (
        window.winfo_screenheight()
    )

    x = (
        screen_width - width
    ) // 2

    y = (
        screen_height - height
    ) // 2

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )

    window.lift()

    try:
        window.attributes(
            "-topmost",
            True,
        )

        window.after(
            200,
            lambda: window.attributes(
                "-topmost",
                False,
            ),
        )

    except tk.TclError:
        pass

    window.focus_force()


class GuiOutputWriter:
    def __init__(
        self,
        app,
        queue,
    ):
        self.app = app
        self.queue = queue

    def write(
        self,
        text,
    ):
        if not text:
            return

        progress_parts = text.split(
            "\r"
        )

        for index, part in enumerate(
            progress_parts
        ):
            if not part:
                continue

            if (
                part.startswith("API 호출:")
                or part.startswith("API 호출")
            ):
                self.queue.put(
                    (
                        "progress",
                        part.strip(),
                    )
                )

                continue

            if index > 0:
                self.queue.put(
                    (
                        "log",
                        part,
                    )
                )

                continue

            self.queue.put(
                (
                    "log",
                    part,
                )
            )

    def flush(self):
        pass


class LogWriter:
    def __init__(
        self,
        app,
    ):
        self.app = app

    def write(
        self,
        text,
    ):
        if not text:
            return

        self.app.append_log(
            text
        )

    def flush(self):
        pass


def truncate_text(
    text,
    max_length,
):
    text = str(text)

    if len(text) <= max_length:
        return text

    return (
        text[:max_length]
        + "..."
    )


def bind_mousewheel(
    widget,
    callback,
):
    def on_enter(event):
        widget.bind_all(
            "<MouseWheel>",
            callback,
        )

        widget.bind_all(
            "<Button-4>",
            callback,
        )

        widget.bind_all(
            "<Button-5>",
            callback,
        )

    def on_leave(event):
        try:
            widget.unbind_all(
                "<MouseWheel>"
            )

            widget.unbind_all(
                "<Button-4>"
            )

            widget.unbind_all(
                "<Button-5>"
            )

        except tk.TclError:
            pass

    widget.bind(
        "<Enter>",
        on_enter,
    )

    widget.bind(
        "<Leave>",
        on_leave,
    )