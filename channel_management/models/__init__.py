from .channel_manager import ChannelManager
from .channel_owner import ChannelOwner, IsOwnerPermission
from .channel_admin import ChannelAdmin, IsAdminPermission
IsManagerPermission = IsOwnerPermission | IsAdminPermission
