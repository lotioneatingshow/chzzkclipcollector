from datetime import datetime


def parse_date(date_string: str):
    """
    치지직 createdDate 문자열을 datetime으로 변환합니다.

    예:
        2026-10-05 14:32:10
    """

    if not date_string:
        return None

    # 이미 datetime인 경우
    if isinstance(date_string, datetime):
        return date_string

    try:
        return datetime.strptime(
            str(date_string).strip(),
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:
        return None


def sort_date(date_string: str):
    """
    클립 정렬용 날짜입니다.

    정상적인 날짜:
        해당 datetime 반환

    잘못된 날짜:
        가장 오래된 날짜 반환
    """

    parsed_date = parse_date(date_string)

    if parsed_date is None:
        return datetime.min

    return parsed_date


def sanitize_filename(filename: str):
    """
    Windows 파일명에 사용할 수 없는 문자를
    '_'로 변경합니다.
    """

    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        filename = filename.replace(
            char,
            "_"
        )

    return filename.strip()