from enum import StrEnum
from typing import NamedTuple


class Attr(NamedTuple):
    key: str
    name: str


class AttrGroup(NamedTuple):
    key: str
    name: str
    children: list[Attr]


class DeviceStatus(StrEnum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    UNDER_MAINTENANCE = "under maintenance"
    RETIRED = "retired"
    LOST = "lost"


DEVICE_STATUS_DISPLAY: dict[str, str] = {
    DeviceStatus.AVAILABLE: "Có sẵn",
    DeviceStatus.ASSIGNED: "Đã bán",
    DeviceStatus.UNDER_MAINTENANCE: "Đang bảo hành",
    DeviceStatus.RETIRED: "Hư hỏng",
    DeviceStatus.LOST: "Mất lạc",
}


DEVICE_STATUS_CHOICES = [(status.value, status.value) for status in DeviceStatus]
