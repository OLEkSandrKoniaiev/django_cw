from enum import Enum


class RegexEnum(Enum):
    PHONE = (
        r'^\+380(39|50|63|66|67|68|73|91|92|93|94|95|96|97|98|99)\d{7}$',
        [
            'Phone number must start with +380',
            'Phone number must contain a valid operator code (39, 50, 63, 66, 67, 68, 73, 91, 92, 93, 94, 95, 96, 97, 98, 99)',
            'Phone number must contain exactly 7 digits after the operator code'
        ]
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg
