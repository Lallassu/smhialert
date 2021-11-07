class SmhiAlertCard extends Polymer.Element {
    static get template() {
        return Polymer.html`
         <style>
          ha-card {
            padding: 16px;
          }
          .box {
            padding: 5px;
            box-shadow: 1px 1px 1px 1px #222222;
          }
          .district {
             font-size: large;
             text-decoration: underline;
             margin-top: 10px;
          }
          .header {
            @apply --paper-font-headline;
            color: var(--primary-text-color);
            padding: 4px 0 12px;
            line-height: 40px;
          }
          .msg {
            font-size: small;
            margin-top: 10px;
            border: 1px;
            border-style: dotted;
            line-height: 17px;
          }
          .noalerts {
            font-size: small;
            margin-top: 10px;
          }
          a {
            color: #FFFFFF;
          }
        </style>
        <ha-card>
          <div class="header">
            <div class="name">
               [[displayName()]]
            </div>
            <template is="dom-if" if="{{_hasNoMessages(stateObj.attributes.messages)}}">
               <span class="noalerts">No current alerts.</span>
            </template>
            <h1>WHAT!</h1>
            <template is="dom-repeat" items="{{stateObj.attributes.messages}}">
              <div class="box">
                 <div><span class="district">{{item.area}}</span></div>
                    <div class="msg" style="color: {{item.event_color}};">
                       <span><b>Event</b>: {{item.event}}<span><br>
                       <span><b>Level</b>: {{item.level}}<span><br>
                       <span><b>Severity</b>: {{item.severity}}<span><br>
                       <span><b>Issued</b>: {{item.published}}</span><br>
                       <span><b>Period</b>: {{item.start}} - {{item.end}}</span><br>
                       <span>{{item.details}}</span>
                    </div>
              </div>
            </template>
          </div>
        </ha-card>
        `;
    }

    static get properties() {
        return {
            _hass: Object,
            _config: Object,
            _stateObj: Object,
            _error: String,
            _test: Array
        }
    }

    _hasNoMessages(x) {
        console.log("X: ", len(x));
        if (x.length > 0) {
            return false;
        }
        return true;
    }

    setConfig(config) {
        this._config = config;
    }

    set hass(hass) {
        this._hass = hass;
        this.stateObj = hass.states[this._config.entity];
        console.log("OBJ:",this.stateObj);
    }

    displayName() {
		return this._config.name || this._config.title || this.stateObj.attributes.friendly_name;
	}


    stopPropagation(e) {
        e.stopPropagation();
    }

}

customElements.define('smhialert-card', SmhiAlertCard);
