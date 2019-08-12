"""

Get weather alerts and warnings from SMHI.

Example configuration

sensor:
  - platform: smhialert

Example advanced configuration

sensor:
  - platform: smhialert

Available districts: See README.md

"""
import logging
import json
from datetime import timedelta

from urllib.request import urlopen

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.components.rest.sensor import RestData

__version__ = '1.0.0'

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'SMHIAlert'

SCAN_INTERVAL = timedelta(minutes=5)

#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#    vol.Optional(CONF_NAME): cv.string,
#})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the SMHIAlert sensor."""
    #name = config.get(CONF_NAME)
    #if config.get(CONF_NAME) is None:
    name = DEFAULT_NAME

    api = SMHIAlert()

    add_entities([SMHIAlertSensor(api, name)], True)


class SMHIAlertSensor(Entity):
    """Representation of a SMHIAlert sensor."""

    def __init__(self, api, name):
        """Initialize a SMHIAlert sensor."""
        self._api = api
        self._name = name
        self._icon = "mdi:alert"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._api.data['state']

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        data = {
            'messages': self._api.attributes['messages']
        }

        return data

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._api.available

    def update(self):
        """Get the latest data from the SMHIAlert API."""
        self._api.update()

class SMHIAlert:
    """Get the latest data and update the states."""

    def __init__(self):
        """Initialize the data object."""
        self.attributes = {}
        self.attributes["messages"] = []
        self.data = {}
        self.available = True
        self.update()
        self.data['state'] = "No Alerts"

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data from SMHIAlert."""
        try:
            response = urlopen('https://opendata-download-warnings.smhi.se/api/version/2/alerts.json')
            data = response.read().decode('utf-8')
            jsondata = json.loads(data)

            self.data['state'] = "No Alerts"
            self.attributes['messages'] = []
            for alert in jsondata['alert']:
                # Skip if status = Actual || System
                #if alert['status'] != 'Actual' or alert['status'] != 'System':
                #    continue

                message = {}

                # Get event name in eng.
                event_type = "unknown"
                for event in alert['info']['eventCode']:
                    if event['valueName'] == "system_event_level":
                        event = event['value']
                        break
                _LOGGER.error(event_type)
                message['event'] = event_type

                # TBD: Skip if expired.
                message['district_code'] = alert['info']['area']['areaDesc']
                message['district_name'] = alert['info']['headline']
                message['identifier'] = alert['identifier']
                message['sent'] = alert['sent']
                message['type'] = alert['msgType']
                message['category'] = alert['info']['category']
                message['certainty'] = alert['info']['certainty']
                message['severity'] = alert['info']['severity']
                message['description'] = alert['info']['description']
                message['link'] = alert['info']['web']
                message['urgency'] = alert['info']['urgency']
                _LOGGER.error(message)
                self.attributes['messages'].append(message)

            self.available = True
            if len(self.attributes['messages']) != 0:
                self.data['state'] = 'Alert'
        except Exception as e:
            _LOGGER.error("Unable to fetch data from SMHI.")
            _LOGGER.error(str(e))
            self.available = False

