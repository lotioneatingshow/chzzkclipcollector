from datetime import datetime

from chzzk_api import (
    get_channel_name,
    get_new_clips,
)

from excel_manager import save_xlsx

from file_manager import (
    find_existing_file,
    get_files_directory,
    load_existing_clips,
)

from gui import run_app


def sanitize_filename(
    filename,
):
    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        filename = filename.replace(
            char,
            "_",
        )

    filename = filename.strip()

    if not filename:
        filename = "unknown"

    return filename


def collect_channel(
    channel_code,
    channel_name=None,
):
    print()

    print(
        f"채널 수집 시작: "
        f"{channel_name or channel_code}"
    )

    print(
        f"채널 코드: {channel_code}"
    )

    print()

    files_directory = (
        get_files_directory()
    )

    existing_file = (
        find_existing_file(
            channel_code,
            files_directory,
        )
    )

    existing_clips = (
        load_existing_clips(
            existing_file
        )
    )

    existing_uids = {
        clip["clip_uid"]
        for clip in existing_clips
    }

    print(
        f"기존 클립: "
        f"{len(existing_clips)}개"
    )

    if existing_file:
        print(
            f"기존 파일: "
            f"{existing_file.name}"
        )

    print()

    new_clips = get_new_clips(
        channel_code,
        existing_uids,
    )

    print()

    if not new_clips:
        print(
            "새로운 클립이 없습니다."
        )

        return

    all_clips = (
        new_clips
        + existing_clips
    )

    all_clips.sort(
        key=lambda clip: clip.get(
            "created_date",
            ""
        ),
        reverse=True,
    )

    if channel_name is None:
        channel_name = (
            get_channel_name(
                channel_code
            )
        )

    if not channel_name:
        channel_name = channel_code

    safe_channel_name = (
        sanitize_filename(
            channel_name
        )
    )

    timestamp = (
        datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    filename = (
        f"{safe_channel_name}_"
        f"{timestamp}_"
        f"{channel_code}.xlsx"
    )

    output_file = (
        files_directory
        / filename
    )

    save_xlsx(
        all_clips,
        output_file,
    )

    if existing_file is not None:
        try:
            if (
                existing_file.resolve()
                != output_file.resolve()
            ):
                existing_file.unlink()

        except OSError as e:
            print(
                f"기존 파일 삭제 실패: {e}"
            )

    print()

    print(
        f"새로운 클립: "
        f"{len(new_clips)}개"
    )

    print(
        f"전체 클립: "
        f"{len(all_clips)}개"
    )

    print(
        f"저장 완료: "
        f"{output_file.name}"
    )


def update_channel(
    channel_code,
    channel_name,
    existing_file,
):
    print()

    print(
        f"채널 최신화 시작: "
        f"{channel_name}"
    )

    print(
        f"채널 코드: {channel_code}"
    )

    print()

    existing_clips = (
        load_existing_clips(
            existing_file
        )
    )

    existing_uids = {
        clip["clip_uid"]
        for clip in existing_clips
    }

    print(
        f"기존 클립: "
        f"{len(existing_clips)}개"
    )

    print(
        f"기존 파일: "
        f"{existing_file.name}"
    )

    print()

    new_clips = get_new_clips(
        channel_code,
        existing_uids,
    )

    print()

    if not new_clips:
        print(
            "새로운 클립이 없습니다."
        )

        return

    all_clips = (
        new_clips
        + existing_clips
    )

    all_clips.sort(
        key=lambda clip: clip.get(
            "created_date",
            ""
        ),
        reverse=True,
    )

    safe_channel_name = (
        sanitize_filename(
            channel_name
        )
    )

    timestamp = (
        datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    filename = (
        f"{safe_channel_name}_"
        f"{timestamp}_"
        f"{channel_code}.xlsx"
    )

    output_file = (
        existing_file.parent
        / filename
    )

    save_xlsx(
        all_clips,
        output_file,
    )

    try:
        if (
            existing_file.resolve()
            != output_file.resolve()
        ):
            existing_file.unlink()

    except OSError as e:
        print(
            f"기존 파일 삭제 실패: {e}"
        )

    print(
        f"새로운 클립: "
        f"{len(new_clips)}개"
    )

    print(
        f"전체 클립: "
        f"{len(all_clips)}개"
    )

    print(
        f"저장 완료: "
        f"{output_file.name}"
    )


def main():
    run_app(
        get_files_directory=(
            get_files_directory
        ),
        get_channel_name=(
            get_channel_name
        ),
        collect_channel=(
            collect_channel
        ),
        update_channel=(
            update_channel
        ),
    )


if __name__ == "__main__":
    main()