BASE_URL = "https://api.chzzk.naver.com"

CLIP_API = (
    BASE_URL
    + "/service/v1/channels/{channel_id}/clips"
)

CHANNEL_API = (
    BASE_URL
    + "/service/v1/channels/{channel_id}"
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}