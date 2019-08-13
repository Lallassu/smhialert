// Windy: <img src="https://img.icons8.com/ultraviolet/40/000000/windy-weather.png">
// Thunder: <img src="https://img.icons8.com/color/50/000000/cloud-lighting.png">
//
// Category:
// Fire: <img src="https://img.icons8.com/color/50/000000/fire-element.png">
// Rescue: <img src="https://img.icons8.com/color/50/000000/fireman-male--v2.png">
// Safety: <img src="https://img.icons8.com/color/50/000000/exit-sign.png">
// Health: <img src="https://img.icons8.com/color/50/000000/health-book.png">
// env: <img src="https://img.icons8.com/dusk/50/000000/environmental-planning.png">
// infra: <img src="https://img.icons8.com/color/50/000000/25-de-abril-bridge.png">
// transport: <img src="https://img.icons8.com/color/50/000000/traffic-jam.png">
// geo: <img src="https://img.icons8.com/color/50/000000/volcano.png">
// met: <img src="https://img.icons8.com/color/50/000000/partly-cloudy-rain.png">
class SmhiAlertCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    setConfig(config) {
        if (!config.district) config.district = 'all';

        const root = this.shadowRoot;
        if (root.lastChild) root.removeChild(root.lastChild);

        const cardConfig = Object.assign({}, config);
        const card = document.createElement('ha-card');
        card.header = config.title;
        const content = document.createElement('div');
        const style = document.createElement('style');
        style.textContent = `
.hover {
}

.tooltip {
  /* hide and position tooltip */
  background-color: black;
  color: white;
  border-radius: 5px;
  opacity: 0;
  position: absolute;
  -webkit-transition: opacity 0.5s;
  -moz-transition: opacity 0.5s;
  -ms-transition: opacity 0.5s;
  -o-transition: opacity 0.5s;
  transition: opacity 0.5s;
}

.hover:hover tr {
  /* display tooltip on hover */
  opacity: 1;
}
.hover:hover .tooltip {
  /* display tooltip on hover */
  opacity: 1;
}
               table {
                 width: 100%;
                 padding: 16px;
               }
               .district {
                   padding-left: 16px;
                   font-size: large;
                   text-decoration: underline;
               }
               thead th {
                 text-align: left;
               }
               tbody tr:nth-child(odd) {
                 background-color: var(--paper-card-background-color);
               }
               tbody tr:nth-child(even) {
                 background-color: var(--secondary-background-color);
               }
             `;
        content.innerHTML = `
         <div id="attributes"></div>
        `;
        card.appendChild(style);
        card.appendChild(content);
        root.appendChild(card)
        this._config = cardConfig;
    }

    _updateContent(element, attributes) {
        const config = this._config;
        let data = "";
        for(var k in attributes) {
              if (config.district != k && config.district != 'all') {
		continue;
		}
              data += "<div class='district hover'>"+attributes[k].name+"<div class='tooltip'>District ID: "+k+"</div></div>";
              data += `<table>
                <thead>
                  <tr>
                    <th>Event</th>
                    <th>Category</th>
                    <th>Severity</th>
                    <th>Urgency</th>
                    <th>Link</th>
                  </tr>
                </thead>
                <tbody>`;
             let msg = attributes[k].messages;
	     for(var v in msg) {
		 data += "<tr style='color:"+msg[v].event_color+";'>";
		 data += "<td>"+msg[v].event+"</td>";
		 data += "<td>"+msg[v].category+"</td>";
		 data += "<td>"+msg[v].severity+"</td>";
		 data += "<td>"+msg[v].urgency+"</td>";
	         data += "<td><a target='_blank' href='"+msg[v].link+"?#ws=wpt-a,proxy=wpt-a,district="+k+",page=wpt-warning-alla'>Read</a></td>";
                 data += "</tr></a>";
             }	
             data += "</tbody></table>";

        }
        element.innerHTML = data;
    }

    set hass(hass) {
        const config = this._config;
        const root = this.shadowRoot;
	//let attributes = Array.from(hass.states["sensor.smhialert"].attributes.messages);
	let attributes = hass.states["sensor.smhialert"].attributes.messages;
        this._updateContent(root.getElementById('attributes'), attributes);
    }

    getCardSize() {
        return 1;
    }
}

customElements.define('smhialert-card', SmhiAlertCard);
