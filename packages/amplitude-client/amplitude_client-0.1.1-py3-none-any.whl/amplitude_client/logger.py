import aiohttp_client
import json
import logging
import enviral
import importlib.resources as pkg_resources
from . import resources

log = logging.getLogger("amplitude-client")

API_URL = "https://api.amplitude.com/2/httpapi"


class AmplitudeLogger:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def log_event(self, event):
        # Amplitude API requires (user_id OR device_id) AND event_type
        user_id = event.get("user_id")
        device_id = event.get("device_id")
        event_type = event.get("event_type")

        if (not user_id and not device_id) or not event_type:
            return

        event = {"api_key": self.api_key, "events": [event]}

        # Validate event against schema
        enviral.validate_object(
            event, json.loads(pkg_resources.read_text(resources, "schema.json"))
        )

        async with aiohttp_client.post(API_URL, data=json.dumps(event)) as resp:
            if resp.status != 200:
                log.warn("Failed to log event", exc_info=True)

        return resp
