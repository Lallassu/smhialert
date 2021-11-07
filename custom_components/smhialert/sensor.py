"""

Get weather alerts and warnings from SMHI.

Example configuration

sensor:
  - platform: smhialert
    district: 'all'

Or specifying a specific district.
sensor:
  - platform: smhialert
    district: '019'

Available districts: See README.md

"""
import logging
import json
from datetime import timedelta

from urllib.request import urlopen

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME)
from homeassistant.util import Throttle

__version__ = '1.0.1'

_LOGGER = logging.getLogger(__name__)

# Using one name to be able to use the custom smhialert-card
NAME = 'SMHIAlert'
CONF_DISTRICT = 'district'
CONF_LANGUAGE = 'language'

SCAN_INTERVAL = timedelta(minutes=5)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_DISTRICT, default='all'): cv.string,
    vol.Optional(CONF_LANGUAGE, default='en'): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    district = config.get(CONF_DISTRICT)
    language = config.get(CONF_LANGUAGE)
    api = SMHIAlert(district, language)

    add_entities([SMHIAlertSensor(api, NAME)], True)


class SMHIAlertSensor(Entity):
    def __init__(self, api, name):
        self._api = api
        self._name = name
        self._icon = "mdi:alert"

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._api.data['state']

    @property
    def device_state_attributes(self):
        data = {
            'messages': self._api.attributes['messages'],
            'notice': self._api.attributes['notice']
        }
        return data

    @property
    def available(self):
        return self._api.available

    def update(self):
        self._api.update()


class SMHIAlert:
    def __init__(self, district, language):
        self.district = district
        self.language = language
        self.attributes = {}
        self.attributes["messages"] = []
        self.attributes["notice"] = ""
        self.data = {}
        self.available = True
        self.update()
        if self.language == 'en':
            self.data['state'] = "No Alerts"
        else:
            self.data['state'] = "Inga varningar"

    @Throttle(SCAN_INTERVAL)
    def update(self):
        try:
            response = urlopen('https://opendata-download-warnings.smhi.se/ibww/api/version/1/warning.json')
            data = response.read().decode('utf-8')
            jsondata = json.loads(data)

            if self.language == 'en':
                self.data['state'] = "No Alerts"
            else:
                self.data['state'] = "Inga varningar"

            self.attributes['messages'] = []
            self.attributes['notice'] = ""

            if len(jsondata) == 0:
                return

            districts = {}
            notice = ""
            alerts = []
            for alert in jsondata:
                areas = []
                for wa in alert["warningAreas"]:
                    areas.append(wa)

                for area in areas:
                    msg = {}
                    msg["event"] = alert["event"][self.language]

                    msg["start"] = area["approximateStart"]
                    msg["published"] = area["published"]

                    msg["code"] = area["warningLevel"]["code"]
                    msg["severity"] = area["warningLevel"][self.language]
                    msg["level"] = area["warningLevel"][self.language]
                    msg["descr"] = area["eventDescription"][self.language]

                    areas = []
                    validArea = False
                    for a in area["affectedAreas"]:
                        if area["id"] == self.district or self.district == 'all':
                            validArea = True
                        areas.append(a[self.language])

                    if not validArea:
                        continue

                    msg["area"] = ''.join(areas)

                    event_type = "unknown"
                    event_color = "#FFFFFF"
                    if msg["code"] == "RED":
                        event_color ="#FF0000"
                    elif msg["code"] == "YELLOW":
                        event_color = "#FFFF00"
                    elif msg["code"] == "ORANGE":
                        event_color = "#FF7F00"

                    if self.language == 'en':
                        notice += '''\
    [{severity}] ({published})
    District: {area}
    Level: {level}
    Type: {event}
    Start: {start}
    Descr:
    {descr}\n'''.format(**msg)
                    else:
                        notice += '''\
    [{severity}] ({published})
    Område: {area}
    Nivå: {level}
    Typ: {event}
    Start: {start}
    Beskrivning:
    {descr}\n'''.format(**msg)


            self.available = True
            if len(districts) != 0:
                self.data['state'] = 'Alert'
                self.attributes['messages'] = districts
                self.attributes['notice'] = notice
        except Exception as e:
            _LOGGER.error("Unable to fetch data from SMHI.")
            _LOGGER.error(str(e))
            self.available = False
