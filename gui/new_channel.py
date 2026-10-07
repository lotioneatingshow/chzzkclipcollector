import tkinter as tk
from tkinter import messagebox


class NewChannelPanel:
    def __init__(
        self,
        parent,
        app,
        files_directory,
    ):
        self.parent = parent
        self.app = app
        self.files_directory = files_directory

        self.pending_channels = []

        self.build_ui()

    def build_ui(self):
        title_label = tk.Label(
            self.parent,
            text="신규 채널 수집",
            font=("맑은 고딕", 18, "bold"),
        )
        title_label.pack(pady=(15, 8))

        description = tk.Label(
            self.parent,
            text="수집할 채널 코드를 추가해주세요.",
            font=("맑은 고딕", 10),
        )
        description.pack(pady=(0, 15))

        input_frame = tk.Frame(self.parent)
        input_frame.pack(fill="x", padx=30)

        tk.Label(
            input_frame,
            text="채널 코드",
            font=("맑은 고딕", 11),
        ).pack(side="left")

        self.channel_entry = tk.Entry(
            input_frame,
            font=("맑은 고딕", 11),
            width=38,
        )
        self.channel_entry.pack(
            side="left",
            padx=(10, 10),
            ipady=4,
        )

        tk.Button(
            input_frame,
            text="추가",
            font=("맑은 고딕", 10),
            width=8,
            command=self.add_channel,
        ).pack(side="left")

        self.channel_entry.bind(
            "<Return>",
            lambda event: self.add_channel(),
        )

        list_title = tk.Label(
            self.parent,
            text="수집 예정 채널",
            font=("맑은 고딕", 11, "bold"),
            anchor="w",
        )
        list_title.pack(
            fill="x",
            padx=30,
            pady=(20, 8),
        )

        list_container = tk.Frame(
            self.parent,
            relief="solid",
            borderwidth=1,
        )
        list_container.pack(
            fill="both",
            expand=True,
            padx=30,
        )

        self.canvas = tk.Canvas(
            list_container,
            highlightthickness=0,
        )

        scrollbar = tk.Scrollbar(
            list_container,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.list_frame = tk.Frame(self.canvas)

        self.list_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.list_frame,
            anchor="nw",
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set,
        )

        self.canvas.bind(
            "<Configure>",
            self.on_canvas_configure,
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="수집 시작",
            font=("맑은 고딕", 11, "bold"),
            width=14,
            height=2,
            command=self.start_collection,
        ).pack(side="left", padx=8)

        tk.Button(
            button_frame,
            text="메뉴로",
            font=("맑은 고딕", 11),
            width=14,
            height=2,
            command=self.back_to_menu,
        ).pack(side="left", padx=8)

        self.refresh_list()
        self.channel_entry.focus_set()

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width,
        )

    def add_channel(self):
        channel_code = self.channel_entry.get().strip()

        if not channel_code:
            messagebox.showwarning(
                "입력 오류",
                "채널 코드를 입력해주세요.",
                parent=self.app.root,
            )
            self.channel_entry.focus_set()
            return

        for code, name in self.pending_channels:
            if code == channel_code:
                messagebox.showwarning(
                    "중복 채널",
                    "이미 추가된 채널입니다.",
                    parent=self.app.root,
                )
                self.channel_entry.focus_set()
                return

        existing_files = self.app.get_existing_channel_files()

        for code, file in existing_files:
            if code == channel_code:
                messagebox.showwarning(
                    "기존 채널",
                    "이미 수집된 채널입니다.\n"
                    "기존 채널 최신화를 이용해주세요.",
                    parent=self.app.root,
                )
                self.channel_entry.focus_set()
                return

        self.app.set_busy(True)

        try:
            channel_name = self.app.get_channel_name(
                channel_code
            )
        finally:
            self.app.set_busy(False)

        if not channel_name:
            messagebox.showerror(
                "채널 조회 실패",
                "채널 정보를 가져오지 못했습니다.\n"
                "채널 코드를 확인해주세요.",
                parent=self.app.root,
            )
            self.channel_entry.focus_set()
            return

        self.pending_channels.append(
            (
                channel_code,
                channel_name,
            )
        )

        self.channel_entry.delete(0, tk.END)
        self.refresh_list()
        self.channel_entry.focus_set()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.pending_channels:
            tk.Label(
                self.list_frame,
                text="추가된 채널이 없습니다.",
                font=("맑은 고딕", 10),
            ).pack(pady=30)

            self.app.apply_theme()
            return

        for index, (
            channel_code,
            channel_name,
        ) in enumerate(self.pending_channels):
            row = tk.Frame(
                self.list_frame,
                pady=7,
            )
            row.pack(
                fill="x",
                padx=10,
            )

            info_frame = tk.Frame(row)
            info_frame.pack(
                side="left",
                fill="x",
                expand=True,
            )

            tk.Label(
                info_frame,
                text=channel_name,
                font=("맑은 고딕", 11, "bold"),
                anchor="w",
            ).pack(fill="x")

            tk.Label(
                info_frame,
                text=channel_code,
                font=("맑은 고딕", 9),
                anchor="w",
            ).pack(fill="x")

            tk.Button(
                row,
                text="취소",
                font=("맑은 고딕", 9),
                width=7,
                command=lambda i=index: self.remove_channel(i),
            ).pack(
                side="right",
                padx=(10, 0),
            )

        self.app.apply_theme()

    def remove_channel(self, index):
        if 0 <= index < len(self.pending_channels):
            del self.pending_channels[index]

        self.refresh_list()

    def start_collection(self):
        if not self.pending_channels:
            messagebox.showwarning(
                "채널 없음",
                "수집할 채널을 하나 이상 추가해주세요.",
                parent=self.app.root,
            )
            return

        self.app.start_new_collection(
            list(self.pending_channels)
        )

    def back_to_menu(self):
        self.app.show_menu()
