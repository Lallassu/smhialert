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
               <span class="msg">No current alerts.</span>
            </template>
            <template is="dom-repeat" items="{{_toArray(stateObj.attributes.messages)}}">
              <div class="box">
                 <div><span class="district">{{item.value.name}}</span></div>
                 <template is="dom-repeat" items="{{item.value.msgs}}">
                    <div class="msg" style="color: {{item.event_color}};">
                       <span><b>Event</b>: {{item.event}}<span><br>
                       <span><b>Severity</b>: {{item.severity}}<span><br>
                       <span><b>Issued</b>: {{item.sent}}</span><br>
                       <span><b>Certainty</b>: {{item.certainty}}</span><br>
                       <span><b>Web Link</b>: <a target="_blank" href="{{item.link}}?#ws=wpt-a,proxy=wpt-a,district={{item.district_code}},page=wpt-warning-alla">Read more</a></span><br>
                       <span><b>Description</b>: {{item.description}}</span>
                    </div>
                 </template>
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
        if (Object.keys(x).length > 0) {
            return false;
        }
        return true;
    }

    _toArray(obj) {
        return Object.keys(obj).map(function(key) {
            return {
                name: key,
                value: obj[key]
            };
        });
    }

    setConfig(config) {
        this._config = config;
    }

    set hass(hass) {
        this._hass = hass;
        this.stateObj = hass.states[this._config.entity];
        console.log(this.stateObj);
    }

    displayName() {
		return this._config.name || this._config.title || this.stateObj.attributes.friendly_name;
	}


    stopPropagation(e) {
        e.stopPropagation();
    }

}

customElements.define('smhialert-card', SmhiAlertCard);
