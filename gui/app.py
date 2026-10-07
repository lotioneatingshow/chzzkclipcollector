import tkinter as tk
from tkinter import messagebox

from .new_channel import NewChannelPanel
from .settings import (
    SettingsWindow,
    load_settings,
    save_settings,
)
from .theme import (
    MAIN_TITLE_FONT,
    get_theme,
    configure_widget_theme,
)
from .update_channel import UpdateChannelPanel
from .widgets import (
    prepare_window,
)
from .worker import (
    WorkerManager,
    get_channel_name,
    run_new_collection,
    run_update_collection,
)


class ClipCollectorApp:
    def __init__(
        self,
        get_files_directory,
        get_channel_name,
        collect_channel,
        update_channel,
    ):
        self.get_files_directory = (
            get_files_directory
        )

        self.get_channel_name = (
            get_channel_name
        )

        self.collect_channel = (
            collect_channel
        )

        self.update_channel = (
            update_channel
        )

        self.files_directory = (
            self.get_files_directory()
        )

        self.settings = load_settings(
            self.files_directory.parent
        )

        self.theme_name = (
            self.settings.get(
                "theme",
                "light",
            )
        )

        self.theme = get_theme(
            self.theme_name
        )

        self.root = tk.Tk()

        prepare_window(
            self.root,
            "치지직 클립 수집기",
            800,
            700,
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close,
        )

        self.worker_running = False

        self.current_panel = None

        self.settings_window = None

        self.lookup_callback = None
        self.lookup_channel_code = None
        self.operation_type = None
        self.operation_result = None

        self.build_layout()

        self.worker = WorkerManager(
            root=self.root,
            on_log=self.append_log,
            on_progress=self.update_progress,
            on_success=self.on_worker_success,
            on_error=self.on_worker_error,
            on_finished=self.on_worker_finished,
        )

        self.show_menu()

        self.apply_theme()

    def build_layout(self):
        self.main_container = tk.Frame(
            self.root,
        )

        self.main_container.pack(
            fill="both",
            expand=True,
        )

        self.header = tk.Frame(
            self.main_container,
        )

        self.header.pack(
            fill="x",
            pady=(12, 5),
        )

        self.title_label = tk.Label(
            self.header,
            text="치지직 클립 수집기",
            font=MAIN_TITLE_FONT,
        )

        self.title_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        self.settings_button = tk.Button(
            self.header,
            text="⚙",
            font=(
                "맑은 고딕",
                14,
            ),
            width=3,
            command=self.open_settings,
            relief="flat",
            bd=0,
        )

        self.settings_button.pack(
            side="right",
            padx=(0, 20),
        )

        self.content_frame = tk.Frame(
            self.main_container,
        )

        self.content_frame.pack(
            fill="both",
            expand=True,
        )

        self.log_frame = tk.Frame(
            self.main_container,
        )

        self.log_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 20),
        )

        progress_header = tk.Frame(
            self.log_frame,
        )

        progress_header.pack(
            fill="x",
            pady=(0, 5),
        )

        self.progress_title = tk.Label(
            progress_header,
            text="진행 상태",
            font=(
                "맑은 고딕",
                10,
                "bold",
            ),
            anchor="w",
        )

        self.progress_title.pack(
            side="left",
        )

        self.progress_label = tk.Label(
            progress_header,
            text="대기 중",
            font=(
                "Consolas",
                9,
            ),
            anchor="e",
        )

        self.progress_label.pack(
            side="right",
        )

        log_title = tk.Label(
            self.log_frame,
            text="실행 로그",
            font=(
                "맑은 고딕",
                10,
                "bold",
            ),
            anchor="w",
        )

        log_title.pack(
            fill="x",
            pady=(3, 5),
        )

        log_container = tk.Frame(
            self.log_frame,
            relief="solid",
            borderwidth=1,
        )

        log_container.pack(
            fill="both",
            expand=True,
        )

        self.log_text = tk.Text(
            log_container,
            font=(
                "Consolas",
                9,
            ),
            state="disabled",
            wrap="word",
        )

        log_scrollbar = tk.Scrollbar(
            log_container,
            command=self.log_text.yview,
        )

        self.log_text.configure(
            yscrollcommand=log_scrollbar.set,
        )

        self.log_text.pack(
            side="left",
            fill="both",
            expand=True,
        )

        log_scrollbar.pack(
            side="right",
            fill="y",
        )

    def get_existing_channel_files(self):
        from file_manager import (
            find_all_channel_files,
        )

        return find_all_channel_files(
            self.files_directory
        )

    def append_log(
        self,
        text,
    ):
        if not text:
            return

        self.log_text.configure(
            state="normal"
        )

        self.log_text.insert(
            tk.END,
            text,
        )

        self.log_text.see(
            tk.END
        )

        self.log_text.configure(
            state="disabled"
        )

    def clear_log(self):
        self.log_text.configure(
            state="normal"
        )

        self.log_text.delete(
            "1.0",
            tk.END,
        )

        self.log_text.configure(
            state="disabled"
        )

        self.progress_label.config(
            text="대기 중"
        )

    def update_progress(
        self,
        text,
    ):
        if not text:
            return

        self.progress_label.config(
            text=text
        )

    def set_busy(
        self,
        busy,
    ):
        self.worker_running = busy

        if busy:
            self.root.config(
                cursor="watch"
            )

        else:
            self.root.config(
                cursor=""
            )

        self.update_button_states()

    def update_button_states(self):
        if self.current_panel is None:
            return

        try:
            if hasattr(
                self.current_panel,
                "add_button",
            ):
                self.current_panel.add_button.config(
                    state=(
                        "disabled"
                        if self.worker_running
                        else "normal"
                    )
                )

        except tk.TclError:
            pass

    def clear_content(self):
        for widget in (
            self.content_frame.winfo_children()
        ):
            widget.destroy()

        self.current_panel = None

    def show_menu(self):
        if self.worker_running:
            return

        self.clear_content()

        menu_frame = tk.Frame(
            self.content_frame,
        )

        menu_frame.pack(
            fill="both",
            expand=True,
        )

        tk.Label(
            menu_frame,
            text="메뉴",
            font=(
                "맑은 고딕",
                15,
                "bold",
            ),
        ).pack(
            pady=(25, 25),
        )

        tk.Button(
            menu_frame,
            text="1. 신규 채널 수집",
            font=(
                "맑은 고딕",
                12,
            ),
            width=24,
            height=2,
            command=self.show_new_channel,
        ).pack(
            pady=8,
        )

        tk.Button(
            menu_frame,
            text="2. 기존 채널 최신화",
            font=(
                "맑은 고딕",
                12,
            ),
            width=24,
            height=2,
            command=self.show_update_channel,
        ).pack(
            pady=8,
        )

        tk.Button(
            menu_frame,
            text="0. 프로그램 종료",
            font=(
                "맑은 고딕",
                12,
            ),
            width=24,
            height=2,
            command=self.close,
        ).pack(
            pady=8,
        )

        self.clear_log()

        self.apply_theme()

    def show_new_channel(self):
        if self.worker_running:
            return

        self.clear_content()

        panel = NewChannelPanel(
            self.content_frame,
            self,
            self.files_directory,
        )

        self.current_panel = panel

        self.clear_log()

        self.apply_theme()

    def show_update_channel(self):
        if self.worker_running:
            return

        self.clear_content()

        panel = UpdateChannelPanel(
            self.content_frame,
            self,
            self.files_directory,
        )

        self.current_panel = panel

        self.clear_log()

        self.apply_theme()

    def start_channel_lookup(
        self,
        channel_code,
        callback,
    ):
        if self.worker_running:
            return

        self.set_busy(
            True
        )

        self.clear_log()

        def lookup():
            return get_channel_name(
                self.get_channel_name,
                channel_code,
            )

        self.lookup_callback = callback
        self.lookup_channel_code = channel_code

        self.worker.start(
            lookup
        )

    def start_new_collection(
        self,
        channels,
    ):
        if self.worker_running:
            return

        self.clear_content()

        self.clear_log()

        self.show_operation_header(
            "신규 채널 수집 진행 중"
        )

        self.set_busy(
            True
        )

        self.operation_type = (
            "new_collection"
        )

        self.worker.start(
            run_new_collection,
            self,
            channels,
        )

    def start_update_collection(
        self,
        channels,
    ):
        if self.worker_running:
            return

        self.clear_content()

        self.clear_log()

        self.show_operation_header(
            "기존 채널 최신화 진행 중"
        )

        self.set_busy(
            True
        )

        self.operation_type = (
            "update_collection"
        )

        self.worker.start(
            run_update_collection,
            self,
            channels,
        )

    def on_worker_success(
        self,
        result,
    ):
        callback = getattr(
            self,
            "lookup_callback",
            None,
        )

        if callable(callback):
            channel_code = getattr(
                self,
                "lookup_channel_code",
                None,
            )

            self.lookup_callback = None
            self.lookup_channel_code = None

            self.set_busy(
                False
            )

            callback(
                channel_code,
                result,
            )

            self.apply_theme()

            return

        self.operation_result = result

    def on_worker_error(
        self,
        error_data,
    ):
        error, traceback_text = (
            error_data
        )

        self.lookup_callback = None
        self.lookup_channel_code = None
        self.operation_result = None

        self.append_log(
            "\n"
            + "=" * 60
            + "\n"
            + "오류가 발생했습니다.\n"
            + f"{error}\n"
            + "\n"
            + "상세 오류:\n"
            + traceback_text
            + "=" * 60
            + "\n"
        )

    def on_worker_finished(self):
        if callable(
            getattr(
                self,
                "lookup_callback",
                None,
            )
        ):
            self.set_busy(
                False
            )

            return

        self.set_busy(
            False
        )

        if getattr(
            self,
            "operation_type",
            None,
        ) == "new_collection":
            self.show_operation_complete(
                "신규 채널 수집이 완료되었습니다."
            )

        elif getattr(
            self,
            "operation_type",
            None,
        ) == "update_collection":
            self.show_operation_complete(
                "선택한 채널 최신화가 완료되었습니다."
            )

        self.operation_type = None

    def show_operation_header(
        self,
        title,
    ):
        frame = tk.Frame(
            self.content_frame,
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        tk.Label(
            frame,
            text=title,
            font=(
                "맑은 고딕",
                17,
                "bold",
            ),
        ).pack(
            pady=(25, 10),
        )

        tk.Label(
            frame,
            text="작업이 진행되는 동안 잠시 기다려주세요.",
            font=(
                "맑은 고딕",
                10,
            ),
        ).pack()

        tk.Label(
            frame,
            text="아래 실행 로그에서 진행 상황을 확인할 수 있습니다.",
            font=(
                "맑은 고딕",
                10,
            ),
        ).pack(
            pady=5,
        )

        self.apply_theme()

    def show_operation_complete(
        self,
        message,
    ):
        for widget in (
            self.content_frame.winfo_children()
        ):
            widget.destroy()

        frame = tk.Frame(
            self.content_frame,
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        tk.Label(
            frame,
            text="작업 완료",
            font=(
                "맑은 고딕",
                18,
                "bold",
            ),
        ).pack(
            pady=(35, 10),
        )

        tk.Label(
            frame,
            text=message,
            font=(
                "맑은 고딕",
                11,
            ),
        ).pack(
            pady=5,
        )

        tk.Button(
            frame,
            text="메뉴로 돌아가기",
            font=(
                "맑은 고딕",
                11,
            ),
            width=18,
            height=2,
            command=self.show_menu,
        ).pack(
            pady=25,
        )

        self.apply_theme()

    def open_settings(self):
        if (
            self.settings_window is not None
            and self.settings_window.window.winfo_exists()
        ):
            self.settings_window.window.lift()
            return

        self.settings_window = SettingsWindow(
            self
        )

    def set_theme(
        self,
        theme_name,
    ):
        if theme_name not in {
            "light",
            "dark",
        }:
            theme_name = "light"

        self.theme_name = theme_name

        self.theme = get_theme(
            theme_name
        )

        self.settings["theme"] = (
            theme_name
        )

        save_settings(
            self.files_directory.parent,
            self.settings,
        )

        self.apply_theme()

    def apply_theme(self):
        self.theme = get_theme(
            self.theme_name
        )

        configure_widget_theme(
            self.root,
            self.theme,
        )

        try:
            self.settings_button.configure(
                background=self.theme["bg"],
                foreground=self.theme["text"],
                activebackground=self.theme["surface"],
                activeforeground=self.theme["text"],
                relief="flat",
                borderwidth=0,
                bd=0,
                highlightthickness=0,
            )

            self.title_label.configure(
                foreground=self.theme["title_text"]
            )

        except tk.TclError:
            pass

        if (
            self.settings_window is not None
            and self.settings_window.window.winfo_exists()
        ):
            try:
                configure_widget_theme(
                    self.settings_window.window,
                    self.theme,
                )
            except tk.TclError:
                pass

        self.root.configure(
            background=self.theme["bg"]
        )

    def close(self):
        if self.worker_running:
            result = messagebox.askyesno(
                "작업 진행 중",
                "현재 작업이 진행 중입니다.\n"
                "프로그램을 종료하시겠습니까?",
                parent=self.root,
            )

            if not result:
                return

        self.root.destroy()

    def run(self):
        self.root.mainloop()


def run_app(
    get_files_directory,
    get_channel_name,
    collect_channel,
    update_channel,
):
    app = ClipCollectorApp(
        get_files_directory,
        get_channel_name,
        collect_channel,
        update_channel,
    )

    app.run()