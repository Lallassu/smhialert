"""

Get weather alerts and warnings from SMHI.

Example configuration

sensor:
  - platform: smhialert
    district: 'all'

Or specifying a specific district.
sensor:
  - platform: smhialert
    district: '19'
    language: 'sv'

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

__version__ = '1.0.2'

_LOGGER = logging.getLogger(__name__)

# Using one name to be able to use the custom smhialert-card
NAME = 'SMHIAlert'
CONF_DISTRICT = 'district'
CONF_LANGUAGE = 'language'

SCAN_INTERVAL = timedelta(minutes=5)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=NAME): cv.string,
    vol.Optional(CONF_DISTRICT, default='all'): cv.string,
    vol.Optional(CONF_LANGUAGE, default='en'): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    district = config.get(CONF_DISTRICT)
    language = config.get(CONF_LANGUAGE)
    name = config.get(CONF_NAME)
    api = SMHIAlert(district, language)

    add_entities([SMHIAlertSensor(api, name)], True)


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
    def extra_state_attributes(self):
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
            msgs = []
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

            notice = ""
            for alert in jsondata:
                areas = []
                for wa in alert["warningAreas"]:
                    areas.append(wa)

                validAreas = []
                for area in areas:
                    for a in area["affectedAreas"]:
                        if str(a["id"]) == self.district or self.district == 'all':
                            validAreas.append(a[self.language])

                    if len(validAreas) == 0:
                        continue

                    msg = {}
                    msg["event"] = alert["event"][self.language]

                    msg["start"] = area["approximateStart"]

                    if "approximateEnd" in area:
                        msg["end"] = area["approximateEnd"]
                    elif self.language == 'en':
                        msg["end"] = 'Unknown'
                    else:
                        msg["end"] = 'Okänt'

                    msg["published"] = area["published"]

                    msg["code"] = area["warningLevel"]["code"]
                    msg["severity"] = area["warningLevel"][self.language]
                    msg["level"] = area["warningLevel"][self.language]
                    msg["descr"] = area["eventDescription"][self.language]

                    # Details
                    details = ""
                    for m in area["descriptions"]:
                        details += "%s: %s\n"%(m["title"][self.language],m["text"][self.language])

                    msg["details"] = details

                    msg["area"] = ", ".join(validAreas)

                    event_type = "unknown"
                    event_color = "#FFFFFF"
                    if msg["code"] == "RED":
                        event_color ="#FF0000"
                    elif msg["code"] == "YELLOW":
                        event_color = "#FFFF00"
                    elif msg["code"] == "ORANGE":
                        event_color = "#FF7F00"

                    msg["event_color"] = event_color

                    if self.language == 'en':
                        notice += '''\
[{severity}] ({published})
District: {area}
Level: {level}
Type: {event}
Start: {start}
End: {end}
{details}\n'''.format(**msg)
                    else:
                        notice += '''\
[{severity}] ({published})
Område: {area}
Nivå: {level}
Typ: {event}
Start: {start}
Slut: {end}
Beskrivning:
{details}\n'''.format(**msg)
                    msgs.append(msg)

            self.available = True
            if notice != "":
                if self.language == 'en':
                  self.data['state'] = "Alert"
                else:
                  self.data['state'] = "Varning"
                self.attributes['messages'] = msgs
                self.attributes['notice'] = notice
        except Exception as e:
            _LOGGER.error("Unable to fetch data from SMHI.")
            _LOGGER.error(str(e))
            self.available = False
