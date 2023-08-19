import dataclasses

from accounts.models import Ghased
from channels.models import Channel


@dataclasses.dataclass
class ManagerData:
    ghased: Ghased
    channel: Channel
