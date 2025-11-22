from enum import Enum


class ErrorCode(Enum):
    """도메인 에러 코드 정의"""

    # User Domain (1xxx)
    USER_CODE_ALREADY_EXISTS = (1001, "User code '{user_code}' already exists", 409)
    USER_NOT_FOUND = (1002, "User not found", 404)

    # Table Domain (2xxx)
    TABLE_NOT_FOUND = (2001, "Table not found", 404)

    # Seat Domain (3xxx)
    SEAT_NOT_FOUND = (3001, "Seat not found", 404)

    # Reservation Domain (4xxx)
    RESERVATION_NOT_FOUND = (4001, "Reservation not found", 404)
    SEAT_ALREADY_RESERVED = (4002, "Seat is already reserved", 409)
    INVALID_RESERVATION_PASSWORD = (4003, "Invalid reservation password", 401)

    # Episode Domain (5xxx)
    EPISODE_NOT_FOUND = (5001, "Episode not found", 404)

    # Zone Domain (6xxx)
    ZONE_NOT_FOUND = (6001, "Zone not found", 404)

    def __init__(self, code: int, message: str, http_status: int):
        self.code = code
        self.message_template = message
        self.status_code = http_status

