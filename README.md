# Home Assistant - SMHI Weather Warnings & Alerts
Retrieve SMHI Warnings & Alerts in Sweden and trigger actions, view in the home assistant dashboard.

This custom component for Home Assistant fetches data from SMHI open API and parses it. The data
is then divided into a hash map of districts and messages per district. The component can be configured
to notify on all warnings or just for a specific district.

*This component is based on https://github.com/isabellaalstrom/sensor.krisinformation*

## Example Configuration

In configuration.yaml for Home Assistant:

Receive all notifications for all districts:
```
sensor:
  - platform: smhialert
    district: 'all'
```
Or specify a specific district as below:
```
sensor:
  - platform: smhialert
    district: '9'
```

Available districts are listed at the bottom of this README.

You can also chose to get the available information in Swedish by adding `language: 'sv'` to your config for the sensor.

## Custom Lovelace Card

Download the smhialert-card.js and place in your *www* folder of Home Assistant.

Configure the UI (raw edit) and add this to the lovelace configuration:
```
resources:
  - type: js
    url: /local/smhialert-card.js
```

Then you can add a custom card with the following settings:
```
entity: sensor.smhialert
title: SMHI Alerts
type: 'custom:smhialert-card'
```

Lovelace card screenshot:

![](https://github.com/lallassu/smhialert/blob/master/smhialert_example3.png)

## Automation Example Configuration

The below example configures an notification both as push notification and as an email notification.
It will use the prefabricated *notice* that is created by the component. It is also possible to 
use the data structure and configure the message manually (*sensor.smhialert.attributes.messages*).

In automations.yaml:
```
- id: smhialert
  alias: 'SMHI Alert'
  initial_state: 'on'
  trigger:
    platform: state
    entity_id: sensor.smhialert
    to: "Alert"
  action:
    - service: notify.push
      data_template:
         title: "SMHI Alert!"
         message: '{{states.sensor.smhialert.attributes.notice}}'
    - service: notify.email
      data_template:
         title: 'SMHI Alert!'
         message: '{{states.sensor.smhialert.attributes.notice}}'
```

Example of full attributes that could be used in the data template is as follows:
```
{
  "messages": {
    "019": {
      "name": "Norrbottens län inland",
      "msgs": [
        {
          "event": "Risk Forest fire",
          "event_color": "#ab56ac",
          "district_code": "019",
          "district_name": "Norrbottens län inland",
          "identifier": "smhi-bpm-1564087965423",
          "sent": "2019-07-25T22:54:41+02:00",
          "type": "Alert",
          "category": "Met",
          "certainty": "Possible",
          "severity": "Severe",
          "description": "När: Tisdag och onsdag\nVar: I den nordöstra delen\nIntensitet: Risken för bränder i skog och mark är lokalt stor\nKommentar: -",
          "link": "http://www.smhi.se/vadret/vadret-i-sverige/Varningar",
          "urgency": "Expected"
        }
      ]
    }
  },
  "notice": "[Severe] (2019-07-25T22:54:41+02:00)\nDistrict: Norrbottens län inland\nType: Alert\nCertainty: Possible\nDescr:\nNär: Tisdag och onsdag\nVar: I den nordöstra delen\nIntensitet: Risken för bränder i skog och mark är lokalt stor\nKommentar: -\nweb: http://www.smhi.se/vadret/vadret-i-sverige/Varningar?#ws=wpt-a,proxy=wpt-a,district=019,page=wpt-warning-alla'\n\n                ",
  "friendly_name": "SMHIAlert",
  "icon": "mdi:alert"
}
```

The *messages* contains an hash of districts (if 'all' is used) and each districts has *msgs* which is an array of all active messages for that district.

## Usage Screenshots
![](https://github.com/lallassu/smhialert/blob/master/smhialert_example1.png)
![](https://github.com/lallassu/smhialert/blob/master/smhialert_example2.png)

## Todo
- Alert if changes has occured. Alert is always triggering when there are _any_ alert and does not
  take changes into account.
- Be able to specify multiple specific districts.

## Areas
The below table is obtained by issuing:
```
$ curl -s https://opendata-download-warnings.smhi.se/ibww/api/version/1/metadata/area.json | jq -r '.[] |  [.id,.sv] | join(", ")' |sort -h
```
List of areas:
```
1, Stockholms län
3, Uppsala län
4, Södermanlands län
5, Östergötlands län
6, Jönköpings län
7, Kronobergs län
8, Kalmar län
9, Gotlands län
10, Blekinge län
12, Skåne län
13, Hallands län
14, Västra Götalands län
17, Värmlands län
18, Örebro län
19, Västmanlands län
20, Dalarnas län
21, Gävleborgs län
22, Västernorrlands län
23, Jämtlands län
24, Västerbottens län
25, Norrbottens län
41, Bottenviken
42, Norra Kvarken
43, Norra Bottenhavet
44, Södra Bottenhavet
45, Ålands hav
46, Skärgårdshavet
47, Finska Viken
48, Norra Östersjön
49, Mellersta Östersjön
50, Rigabukten
51, Sydöstra Östersjön
52, Södra Östersjön
53, Sydvästra Östersjön
54, Bälten
55, Öresund
56, Kattegatt
57, Skagerrak
58, Vänern
```
Example Automation

```Yaml
alias: "Notification: Weather Alert"
description: "Alerts if an event happens"
trigger:
  - platform: state
    entity_id:
      - sensor.weather_alert.<yourarea>
    to: "Alert"
    from: null
condition: []
action:
  - service: notify.<device>
    data:
      message: >-
        {% set alerts = state_attr('sensor.weather_alert', 'messages') %}
        {% for alert in alerts %}
          There is a weather alert for the area of {{ alert.area }}. The event is classified as {{ alert.event }} with a severity level of {{ alert.severity }}. {{ alert.details.split('\n\n')[0].replace('What happens?: ', '') }}
        {% endfor %}
      data:
        channel: updates
        timeout: 900
        visibility: public
        alert_once: true
        subject: Weather Alert
        importance: high
        notification_icon: mdi:weather-sunny
        icon_url: >-
          https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather02-512.png
```
Replace `sensor.weather_alert.<yourarea>` with your actual sensor and ` service: notify.<device>` with your actual device
