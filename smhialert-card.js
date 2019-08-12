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
        if (!config.district) config.district = 'All';
        console.log("district:",config.district);

        const root = this.shadowRoot;
        if (root.lastChild) root.removeChild(root.lastChild);

        const cardConfig = Object.assign({}, config);
        const card = document.createElement('ha-card');
        card.header = config.title;
        const content = document.createElement('div');
        const style = document.createElement('style');
        style.textContent = `
               .ico {
                 display: inline-block;
                 background-repeat: no-repeat;
                 background-size: 5px 5px;
                 background: url("https://img.icons8.com/color/50/000000/partly-cloudy-rain.png");
               }
               .windy {
                 background-image: url("https://img.icons8.com/ultraviolet/40/000000/windy-weather.png");
               }
               .thunder {
                 background-image: url("https://img.icons8.com/color/50/000000/cloud-lighting.png");
               }
               .Fire {
                    background-image: url("https://img.icons8.com/color/50/000000/fire-element.png");
               }
               .Rescue {
                    background-image: url("https://img.icons8.com/color/50/000000/fireman-male--v2.png");
               }
               .Safety {
                    background-image: url("https://img.icons8.com/color/50/000000/exit-sign.png");
               }
               .Health {
                    background-image: url("https://img.icons8.com/color/50/000000/health-book.png");
               }
               .Env {
                    background-image: url("https://img.icons8.com/dusk/50/000000/environmental-planning.png");
               }
               .Infra {
                    background-image: url("https://img.icons8.com/color/50/000000/25-de-abril-bridge.png");
               }
               .Transport {
                    background-image: url("https://img.icons8.com/color/50/000000/traffic-jam.png");
               }
               .Geo {
                    background-image: url("https://img.icons8.com/color/50/000000/volcano.png"");
               }
               .Met {
                    background-image: url("https://img.icons8.com/color/50/000000/partly-cloudy-rain.png");
               }

               table {
                 width: 100%;
                 padding: 16px;
               }
               .unknown {
                  color: #000000;
               }
               .Minor {
              color: #00FF00;
               }
               .Extreme {
              color: #FF0000;
               }
               .Moderate {
              color: #FF00FF;
               }
               .Severe {
              color: #FFFF00;
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
              <table>
                <thead>
                  <tr>
                    <th>District</th>
                    <th>Event</th>
                    <th>Category</th>
                    <th>Severity</th>
                    <th>Urgency</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody id='attributes'>
                </tbody>
              </table>
              `;
        card.appendChild(style);
        card.appendChild(content);
        root.appendChild(card)
        this._config = cardConfig;
    }

    _updateContent(element, attributes) {
        element.innerHTML = `
              <tr>
                ${attributes.map((attribute) => `
                  <tr>
                    <td>${attribute.district_name}</td>
                    <td>${attribute.event}</td>
                    <td><span class="ico ${attribute.category}"></span>${attribute.category}</td>
                    <td class="${attribute.severity}">${attribute.severity}</td>
                    <td>${attribute.urgency}</td>
                    <td>${attribute.sent}</td>
                  </tr>
                `).join('')}
              `;
    }

    set hass(hass) {
        const config = this._config;
        const root = this.shadowRoot;
        console.log(hass.states["sensor.smhialert"]);
	let attributes = Array.from(hass.states["sensor.smhialert"].attributes.messages);
        this._updateContent(root.getElementById('attributes'), attributes);
    }

    getCardSize() {
        return 1;
    }
}

customElements.define('smhialert-card', SmhiAlertCard);
