import dataclasses


@dataclasses.dataclass
class GhasedData:
    username: str
    phone_number: str
    email: str
    password: str
