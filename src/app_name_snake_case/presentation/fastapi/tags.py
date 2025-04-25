from enum import Enum


class Tag(Enum):
    user = "User"
    monitoring = "Monitoring"


tags_metadata = [
    {
        "name": Tag.user.value,
        "description": "Current user endpoints.",
    },
    {
        "name": Tag.monitoring.value,
        "description": "Endpoints for monitoring.",
    },
]
