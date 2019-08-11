"""

Get weather alerts and warnings from SMHI.

Example configuration

sensor:
  - platform: smhialert

Example advanced configuration

sensor:
  - platform: smhialert
    district: '019'

Available districts: See README.md

"""
import logging
import json
from datetime import timedelta
#from math import radians, sin, cos, acos
#import requests

from urllib.request import urlopen
#import aiohttp

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME, CONF_RADIUS)
from homeassistant.util import Throttle
import homeassistant.util.dt as dt_util
from homeassistant.components.rest.sensor import RestData

__version__ = '1.0.0'

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'SMHIAlert'
DEFAULT_DISTRICT = 'all'
CONF_DISTRICT = 'district'

SCAN_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_DISTRICT) : cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the SMHIAlert sensor."""
    name = config.get(CONF_NAME)
    district = config.get(CONF_DISTRICT)
    if config.get(CONF_NAME) is None:
        name = DEFAULT_NAME
    if config.get(CONF_DISTRICT) is None:
        name = DEFAULT_DISTRICT

    api = SMHIAlert(district)

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

    def __init__(self, district):
        """Initialize the data object."""
        self.district = district
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
                message = {}
                district = alert['info']['area']['areaDesc']
                if district == self.district or self.district == 'all':
                    message['district_code'] = district
                    message['district_name'] = alert['info']['headline']
                    message['identifier'] = alert['identifier']
                    message['sent'] = alert['sent']
                    message['type'] = alert['msgType']
                    message['status'] = alert['status']
                    message['event'] = alert['info']['event']
                    message['severity'] = alert['info']['severity']
                    message['description'] = alert['info']['description']
                    message['link'] = alert['info']['web']
                    self.attributes['messages'].append(message)
            self.available = True
            if self.attributes['messages'].len() != 0:
                self.data['state'] = 'Alert'
        except Exception as e:
            _LOGGER.error("Unable to fetch data from SMHI.")
            self.available = False

