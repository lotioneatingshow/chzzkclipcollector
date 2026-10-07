import tkinter as tk
from tkinter import messagebox


PAGE_SIZE = 10
COLUMN_COUNT = 2
ROWS_PER_PAGE = 5


class UpdateChannelPanel:
    def __init__(
        self,
        parent,
        app,
        files_directory,
    ):
        self.parent = parent
        self.app = app
        self.files_directory = files_directory

        self.channels = []
        self.selected_channels = set()
        self.check_vars = {}
        self.current_page = 1
        self.search_keyword = ""

        self.search_entry = None
        self.clear_search_button = None
        self.list_frame = None
        self.page_label = None
        self.prev_button = None
        self.next_button = None

        self.load_channels()
        self.build_ui()
        self.refresh_list()

    def load_channels(self):
        files = self.app.get_existing_channel_files()

        self.channels.clear()

        for channel_code, file in files:
            channel_name = self.get_channel_name_from_file(file)

            self.channels.append(
                {
                    "channel_code": channel_code,
                    "channel_name": channel_name,
                    "file": file,
                }
            )

        self.channels.sort(
            key=lambda channel: channel["channel_name"].casefold()
        )

    @staticmethod
    def get_channel_name_from_file(file):
        stem = file.stem
        parts = stem.rsplit("_", 3)

        if len(parts) == 4:
            return parts[0]

        return stem

    def build_ui(self):
        tk.Label(
            self.parent,
            text="기존 채널 최신화",
            font=("맑은 고딕", 18, "bold"),
        ).pack(
            pady=(15, 5)
        )

        tk.Label(
            self.parent,
            text="최신화할 채널을 선택해주세요.",
            font=("맑은 고딕", 10),
        ).pack(
            pady=(0, 10)
        )

        search_frame = tk.Frame(self.parent)
        search_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 8),
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=("맑은 고딕", 10),
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=5,
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_channels(),
        )

        tk.Button(
            search_frame,
            text="검색",
            font=("맑은 고딕", 9),
            width=8,
            command=self.search_channels,
        ).pack(
            side="left",
            padx=(7, 0),
        )

        self.clear_search_button = tk.Button(
            search_frame,
            text="X",
            font=("맑은 고딕", 9, "bold"),
            width=4,
            command=self.clear_search,
        )
        self.clear_search_button.pack_forget()

        control_frame = tk.Frame(self.parent)
        control_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 8),
        )

        tk.Button(
            control_frame,
            text="전체 선택",
            font=("맑은 고딕", 9),
            width=10,
            command=self.select_all,
        ).pack(
            side="left",
            padx=(0, 5),
        )

        tk.Button(
            control_frame,
            text="전체 해제",
            font=("맑은 고딕", 9),
            width=10,
            command=self.deselect_all,
        ).pack(
            side="left"
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

        self.list_frame = tk.Frame(
            list_container
        )
        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5,
        )

        for column in range(COLUMN_COUNT):
            self.list_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="channel_column",
            )

        for row in range(ROWS_PER_PAGE):
            self.list_frame.grid_rowconfigure(
                row,
                weight=1,
                minsize=44,
            )

        pagination_frame = tk.Frame(self.parent)
        pagination_frame.pack(
            pady=(8, 3)
        )

        self.prev_button = tk.Button(
            pagination_frame,
            text="이전",
            font=("맑은 고딕", 9),
            width=8,
            command=self.previous_page,
        )
        self.prev_button.pack(
            side="left",
            padx=5,
        )

        self.page_label = tk.Label(
            pagination_frame,
            text="1 / 1",
            font=("맑은 고딕", 9),
            width=10,
        )
        self.page_label.pack(
            side="left"
        )

        self.next_button = tk.Button(
            pagination_frame,
            text="다음",
            font=("맑은 고딕", 9),
            width=8,
            command=self.next_page,
        )
        self.next_button.pack(
            side="left",
            padx=5,
        )

        button_frame = tk.Frame(self.parent)
        button_frame.pack(
            pady=(5, 12)
        )

        tk.Button(
            button_frame,
            text="최신화 시작",
            font=("맑은 고딕", 11, "bold"),
            width=14,
            height=2,
            command=self.start_update,
        ).pack(
            side="left",
            padx=8,
        )

        tk.Button(
            button_frame,
            text="메뉴로",
            font=("맑은 고딕", 11),
            width=14,
            height=2,
            command=self.back_to_menu,
        ).pack(
            side="left",
            padx=8,
        )

    def get_filtered_channels(self):
        keyword = (
            self.search_keyword
            .strip()
            .casefold()
        )

        if not keyword:
            return list(self.channels)

        return [
            channel
            for channel in self.channels
            if keyword
            in channel["channel_name"].casefold()
        ]

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.check_vars.clear()

        for row in range(ROWS_PER_PAGE):
            self.list_frame.grid_rowconfigure(
                row,
                weight=1,
                minsize=44,
            )

        filtered_channels = self.get_filtered_channels()
        total_count = len(filtered_channels)

        if total_count == 0:
            tk.Label(
                self.list_frame,
                text=(
                    "검색 결과가 없습니다."
                    if self.search_keyword
                    else "저장된 채널이 없습니다."
                ),
                font=("맑은 고딕", 10),
            ).grid(
                row=0,
                column=0,
                columnspan=COLUMN_COUNT,
                pady=35,
            )

            self.update_pagination(0)
            self.app.apply_theme()
            return

        total_pages = (
            (total_count + PAGE_SIZE - 1)
            // PAGE_SIZE
        )

        if self.current_page > total_pages:
            self.current_page = total_pages

        if self.current_page < 1:
            self.current_page = 1

        start_index = (
            (self.current_page - 1)
            * PAGE_SIZE
        )

        end_index = start_index + PAGE_SIZE

        page_channels = filtered_channels[
            start_index:end_index
        ]

        for index, channel in enumerate(page_channels):
            row = index // COLUMN_COUNT
            column = index % COLUMN_COUNT

            self.create_channel_row(
                channel,
                row,
                column,
            )

        self.update_pagination(total_pages)
        self.app.apply_theme()

    def create_channel_row(
        self,
        channel,
        row,
        column,
    ):
        channel_code = channel["channel_code"]

        cell = tk.Frame(
            self.list_frame,
            height=40,
        )

        cell.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=5,
            pady=2,
        )

        cell.grid_propagate(False)

        var = tk.BooleanVar(
            value=(
                channel_code
                in self.selected_channels
            )
        )

        self.check_vars[channel_code] = var

        var.trace_add(
            "write",
            lambda *args,
            code=channel_code,
            variable=var: self.on_check_changed(
                code,
                variable,
            ),
        )

        tk.Checkbutton(
            cell,
            variable=var,
        ).pack(
            side="left"
        )

        name_label = tk.Label(
            cell,
            text=channel["channel_name"],
            font=("맑은 고딕", 11),
            anchor="w",
        )
        name_label.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 5),
        )

        name_label.bind(
            "<Button-1>",
            lambda event, variable=var: variable.set(
                not variable.get()
            ),
        )

    def on_check_changed(
        self,
        channel_code,
        variable,
    ):
        if variable.get():
            self.selected_channels.add(
                channel_code
            )
        else:
            self.selected_channels.discard(
                channel_code
            )

    def update_pagination(self, total_pages):
        if total_pages <= 0:
            total_pages = 1

        self.page_label.config(
            text=(
                f"{self.current_page} / "
                f"{total_pages}"
            )
        )

        self.prev_button.config(
            state=(
                "disabled"
                if self.current_page <= 1
                else "normal"
            )
        )

        self.next_button.config(
            state=(
                "disabled"
                if self.current_page >= total_pages
                else "normal"
            )
        )

    def previous_page(self):
        if self.current_page <= 1:
            return

        self.current_page -= 1
        self.refresh_list()

    def next_page(self):
        filtered_channels = (
            self.get_filtered_channels()
        )

        total_count = len(filtered_channels)

        total_pages = (
            (total_count + PAGE_SIZE - 1)
            // PAGE_SIZE
        )

        if self.current_page >= total_pages:
            return

        self.current_page += 1
        self.refresh_list()

    def search_channels(self):
        self.search_keyword = (
            self.search_entry.get().strip()
        )

        self.current_page = 1

        if self.search_keyword:
            self.clear_search_button.pack(
                side="left",
                padx=(5, 0),
            )
        else:
            self.clear_search_button.pack_forget()

        self.refresh_list()

    def clear_search(self):
        self.search_keyword = ""

        self.search_entry.delete(
            0,
            tk.END,
        )

        self.clear_search_button.pack_forget()

        self.current_page = 1
        self.refresh_list()
        self.search_entry.focus_set()

    def select_all(self):
        filtered_channels = (
            self.get_filtered_channels()
        )

        for channel in filtered_channels:
            self.selected_channels.add(
                channel["channel_code"]
            )

        self.refresh_list()

    def deselect_all(self):
        filtered_channels = (
            self.get_filtered_channels()
        )

        for channel in filtered_channels:
            self.selected_channels.discard(
                channel["channel_code"]
            )

        self.refresh_list()

    def start_update(self):
        selected_channels = []

        for channel in self.channels:
            if (
                channel["channel_code"]
                in self.selected_channels
            ):
                selected_channels.append(
                    channel
                )

        if not selected_channels:
            messagebox.showwarning(
                "채널 없음",
                "최신화할 채널을 하나 이상 선택해주세요.",
                parent=self.app.root,
            )
            return

        self.app.start_update_collection(
            selected_channels
        )

    def back_to_menu(self):
        self.app.show_menu()