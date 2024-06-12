from enum import Enum


class USER_ROLES(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"


class SORT_TYPE(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class USER_STATUS(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


DOCS_REQUIRE_AUTHORIZED = {
    "Authorization": {
        "description": "Authorization: Bearer asdf.qwer.zxcv",
        "in": "header",
        "type": "string",
        "required": True,
    }
}


regex_password = (
    "^(?=.*[a-zA-Z0-9])(?=.*[!@#$%^&*()_+\\-=\[\]{};':\"\\|,.<>\/?]).{6,20}$"
)

MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50MB

IMAGE_PATH = "images"

IMAGE_TYPE_MAP = {
    "PNG": "image/png",
    "JPG": "image/jpg",
    "JPEG": "image/jpeg",
}
