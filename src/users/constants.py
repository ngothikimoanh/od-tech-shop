from enum import StrEnum

PHONE_NUMBER_REGEX = r"^0\d{9}$"
DEFAULT_FULL_NAME = "Chưa cập nhật tên!"


class Role(StrEnum):
    ADMIN = "admin"
    GUEST = "guest"
    EMPLOYEE = "employee"


ROLE_DISPLAY: dict[str, str] = {
    Role.ADMIN: "Quản trị viên",
    Role.GUEST: "Khách hàng",
    Role.EMPLOYEE: "Nhân viên",
}

ROLE_NOT_INCLUDE_ADMIN = ROLE_DISPLAY.copy()
del ROLE_NOT_INCLUDE_ADMIN[Role.ADMIN]
