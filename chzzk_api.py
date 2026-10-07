import time
import requests

from config import (
    CHANNEL_API,
    CLIP_API,
    HEADERS,
)


MAX_RETRIES = 3

RETRY_DELAYS = [
    2,
    5,
    10,
]


def get_channel_name(channel_id: str):
    url = CHANNEL_API.format(channel_id=channel_id)

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10,
            )

            response.raise_for_status()

            result = response.json()

            if result.get("code") != 200:
                print(
                    f"\n채널 정보 조회 실패: "
                    f"{result.get('message', '알 수 없는 오류')}"
                )
                return None

            content = result.get("content")

            if not content:
                print("\n채널 정보가 없습니다.")
                return None

            return content.get("channelName")

        except requests.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                print(
                    f"\n채널 정보 조회 실패 "
                    f"({attempt + 1}/{MAX_RETRIES})"
                )
                time.sleep(RETRY_DELAYS[attempt])
            else:
                print(
                    f"\n채널 정보 조회 실패: {e}"
                )

        except ValueError:
            print("\n채널 정보 응답을 JSON으로 변환하지 못했습니다.")
            return None

    return None


def print_progress(
    api_call_count: int,
    collected_count: int,
    processed_count: int,
):
    message = (
        f"\rAPI 호출: {api_call_count}회"
        f" | 수집: {collected_count}개"
        f" | 처리: {processed_count}개"
    )

    print(
        message,
        end="",
        flush=True,
    )


def get_new_clips(
    channel_id: str,
    existing_uids: set,
):
    url = CLIP_API.format(channel_id=channel_id)

    new_clips = []

    next_clip_uid = None

    # 진행률
    api_call_count = 0

    # API 응답으로 실제 받은 클립 데이터 수
    collected_count = 0

    # 기존 데이터와 비교하여 신규로 추가된 클립 수
    processed_count = 0

    while True:
        params = {
            "filterType": "ALL",
            "orderType": "RECENT",
            "size": 50,
        }

        if next_clip_uid:
            params["clipUID"] = next_clip_uid

        response = None

        # API 요청
        for attempt in range(MAX_RETRIES):
            try:
                api_call_count += 1

                print_progress(
                    api_call_count,
                    collected_count,
                    processed_count,
                )

                response = requests.get(
                    url,
                    headers=HEADERS,
                    params=params,
                    timeout=10,
                )

                response.raise_for_status()

                break

            except requests.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    print(
                        f"\nAPI 요청 실패 "
                        f"({attempt + 1}/{MAX_RETRIES})"
                    )
                    time.sleep(RETRY_DELAYS[attempt])
                else:
                    print(
                        f"\nAPI 요청 최종 실패: {e}"
                    )
                    print()

                    return new_clips

        try:
            result = response.json()

        except ValueError:
            print("\nAPI 응답을 JSON으로 변환하지 못했습니다.")
            print()

            return new_clips

        if result.get("code") != 200:
            print(
                f"\n클립 조회 실패: "
                f"{result.get('message', '알 수 없는 오류')}"
            )
            print()

            return new_clips

        content = result.get("content")

        if not content:
            break

        data = content.get("data", [])

        if not data:
            break

        # API에서 실제로 받은 데이터 개수
        collected_count += len(data)

        stop = False

        for clip in data:
            clip_uid = clip.get("clipUID")

            if not clip_uid:
                continue

            # 기존 클립을 만나면 이후 데이터는 모두 기존 데이터이므로 종료
            if clip_uid in existing_uids:
                stop = True
                break

            new_clips.append(
                {
                    "title": clip.get("clipTitle", ""),
                    "url": (
                        f"https://chzzk.naver.com/clips/"
                        f"{clip_uid}"
                    ),
                    "clip_uid": clip_uid,
                    "created_date": clip.get("createdDate", ""),
                }
            )

            # 실제로 새로 추가되는 클립 수
            processed_count += 1

        print_progress(
            api_call_count,
            collected_count,
            processed_count,
        )

        if stop:
            break

        next_data = content.get("page", {}).get("next")

        if not next_data:
            break

        next_cursor = next_data.get("clipUID")

        if not next_cursor:
            break

        if next_cursor == next_clip_uid:
            break

        next_clip_uid = next_cursor

        time.sleep(0.2)

    print()

    return new_clips