import contextlib
import queue
import threading
import time
import traceback
import sys


class WorkerOutputWriter:
    def __init__(
        self,
        result_queue,
    ):
        self.result_queue = result_queue

    def write(
        self,
        text,
    ):
        if not text:
            return

        parts = text.split(
            "\r"
        )

        for part in parts:
            if not part:
                continue

            stripped = part.strip()

            if (
                stripped.startswith("API 호출:")
                or stripped.startswith("API 호출")
            ):
                self.result_queue.put(
                    (
                        "progress",
                        stripped,
                    )
                )

            else:
                self.result_queue.put(
                    (
                        "log",
                        part,
                    )
                )

    def flush(self):
        pass


class WorkerManager:
    def __init__(
        self,
        root,
        on_log,
        on_progress,
        on_success,
        on_error,
        on_finished,
    ):
        self.root = root

        self.on_log = on_log
        self.on_progress = on_progress
        self.on_success = on_success
        self.on_error = on_error
        self.on_finished = on_finished

        self.queue = queue.Queue()

        self.thread = None
        self.running = False

        self.root.after(
            50,
            self.process_queue,
        )

    def start(
        self,
        target,
        *args,
        **kwargs,
    ):
        if self.running:
            return False

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            args=(
                target,
                args,
                kwargs,
            ),
            daemon=True,
        )

        self.thread.start()

        return True

    def _run(
        self,
        target,
        args,
        kwargs,
    ):
        writer = WorkerOutputWriter(
            self.queue
        )

        previous_stdout = sys.stdout
        previous_stderr = sys.stderr

        try:
            with contextlib.redirect_stdout(
                writer
            ):
                with contextlib.redirect_stderr(
                    writer
                ):
                    result = target(
                        *args,
                        **kwargs,
                    )

            self.queue.put(
                (
                    "success",
                    result,
                )
            )

        except Exception as e:
            self.queue.put(
                (
                    "error",
                    (
                        e,
                        traceback.format_exc(),
                    ),
                )
            )

        finally:
            sys.stdout = previous_stdout
            sys.stderr = previous_stderr

            self.queue.put(
                (
                    "finished",
                    None,
                )
            )

    def process_queue(self):
        try:
            while True:
                event_type, data = (
                    self.queue.get_nowait()
                )

                if event_type == "log":
                    self.on_log(
                        data
                    )

                elif event_type == "progress":
                    self.on_progress(
                        data
                    )

                elif event_type == "success":
                    self.on_success(
                        data
                    )

                elif event_type == "error":
                    self.on_error(
                        data
                    )

                elif event_type == "finished":
                    self.running = False

                    self.on_finished()

        except queue.Empty:
            pass

        try:
            self.root.after(
                50,
                self.process_queue,
            )

        except Exception:
            pass


def run_new_collection(
    app,
    channels,
):
    total_channels = len(channels)

    for index, (
        channel_code,
        channel_name,
    ) in enumerate(
        channels,
        start=1,
    ):
        print()
        print(
            "=" * 60
        )

        print(
            f"[{index}/{total_channels}] "
            f"{channel_name}"
        )

        print(
            "=" * 60
        )

        app.collect_channel(
            channel_code,
            channel_name,
        )

        print()

        if index < total_channels:
            time.sleep(1.0)


def run_update_collection(
    app,
    channels,
):
    total_channels = len(channels)

    for index, channel in enumerate(
        channels,
        start=1,
    ):
        print()
        print(
            "=" * 60
        )

        print(
            f"[{index}/{total_channels}] "
            f"{channel['channel_name']}"
        )

        print(
            "=" * 60
        )

        app.update_channel(
            channel["channel_code"],
            channel["channel_name"],
            channel["file"],
        )

        print()

        if index < total_channels:
            time.sleep(1.0)


def get_channel_name(
    get_channel_name_function,
    channel_code,
):
    return get_channel_name_function(
        channel_code
    )