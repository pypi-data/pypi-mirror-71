/*! For license information please see chunk.164e471d005092847929.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[37],{208:function(e,t,i){"use strict";i.d(t,"a",function(){return a});var n=i(10);const r=new WeakMap,a=Object(n.f)(e=>t=>{const i=r.get(t);if(void 0===e&&t instanceof n.a){if(void 0!==i||!r.has(t)){const e=t.committer.name;t.committer.element.removeAttribute(e)}}else e!==i&&t.setValue(e);r.set(t,e)})},215:function(e,t,i){"use strict";i.d(t,"b",function(){return n}),i.d(t,"a",function(){return r});const n=(e,t)=>e<t?-1:e>t?1:0,r=(e,t)=>n(e.toLowerCase(),t.toLowerCase())},297:function(e,t,i){"use strict";var n=i(4),r=i(31),a=i(204),o=i(126);i(298),i(216);customElements.define("state-info",class extends r.a{static get template(){return n.a`
      ${this.styleTemplate} ${this.stateBadgeTemplate} ${this.infoTemplate}
    `}static get styleTemplate(){return n.a`
      <style>
        :host {
          @apply --paper-font-body1;
          min-width: 120px;
          white-space: nowrap;
        }

        state-badge {
          float: left;
        }

        :host([rtl]) state-badge {
          float: right;
        }

        .info {
          margin-left: 56px;
        }

        :host([rtl]) .info {
          margin-right: 56px;
          margin-left: 0;
          text-align: right;
        }

        .name {
          @apply --paper-font-common-nowrap;
          color: var(--primary-text-color);
          line-height: 40px;
        }

        .name[in-dialog],
        :host([secondary-line]) .name {
          line-height: 20px;
        }

        .time-ago,
        .extra-info,
        .extra-info > * {
          @apply --paper-font-common-nowrap;
          color: var(--secondary-text-color);
        }
      </style>
    `}static get stateBadgeTemplate(){return n.a` <state-badge state-obj="[[stateObj]]"></state-badge> `}static get infoTemplate(){return n.a`
      <div class="info">
        <div class="name" in-dialog$="[[inDialog]]">
          [[computeStateName(stateObj)]]
        </div>

        <template is="dom-if" if="[[inDialog]]">
          <div class="time-ago">
            <ha-relative-time
              hass="[[hass]]"
              datetime="[[stateObj.last_changed]]"
            ></ha-relative-time>
          </div>
        </template>
        <template is="dom-if" if="[[!inDialog]]">
          <div class="extra-info"><slot> </slot></div>
        </template>
      </div>
    `}static get properties(){return{hass:Object,stateObj:Object,inDialog:{type:Boolean,value:()=>!1},rtl:{type:Boolean,reflectToAttribute:!0,computed:"computeRTL(hass)"}}}computeStateName(e){return Object(a.a)(e)}computeRTL(e){return Object(o.a)(e)}})},298:function(e,t,i){"use strict";var n=i(3),r=i(31),a=i(299),o=i(206);customElements.define("ha-relative-time",class extends(Object(o.a)(r.a)){static get properties(){return{hass:Object,datetime:{type:String,observer:"datetimeChanged"},datetimeObj:{type:Object,observer:"datetimeObjChanged"},parsedDateTime:Object}}constructor(){super(),this.updateRelative=this.updateRelative.bind(this)}connectedCallback(){super.connectedCallback(),this.updateInterval=setInterval(this.updateRelative,6e4)}disconnectedCallback(){super.disconnectedCallback(),clearInterval(this.updateInterval)}datetimeChanged(e){this.parsedDateTime=e?new Date(e):null,this.updateRelative()}datetimeObjChanged(e){this.parsedDateTime=e,this.updateRelative()}updateRelative(){const e=Object(n.a)(this);this.parsedDateTime?e.innerHTML=Object(a.a)(this.parsedDateTime,this.localize):e.innerHTML=this.localize("ui.components.relative_time.never")}})},299:function(e,t,i){"use strict";i.d(t,"a",function(){return a});const n=[60,60,24,7],r=["second","minute","hour","day"];function a(e,t,i={}){let a=((i.compareTime||new Date).getTime()-e.getTime())/1e3;const o=a>=0?"past":"future";let s;a=Math.abs(a);for(let c=0;c<n.length;c++){if(a<n[c]){a=Math.floor(a),s=t(`ui.components.relative_time.duration.${r[c]}`,"count",a);break}a/=n[c]}return void 0===s&&(s=t("ui.components.relative_time.duration.week","count",a=Math.floor(a))),!1===i.includeTense?s:t(`ui.components.relative_time.${o}`,"time",s)}},514:function(e,t,i){"use strict";i.d(t,"b",function(){return r}),i.d(t,"a",function(){return a});var n=i(151);const r=e=>e.include_domains.length+e.include_entities.length+e.exclude_domains.length+e.exclude_entities.length===0,a=(e,t,i,r)=>{const a=new Set(e),o=new Set(t),s=new Set(i),c=new Set(r),l=a.size>0||o.size>0,d=s.size>0||c.size>0;return l||d?l&&!d?e=>o.has(e)||a.has(Object(n.a)(e)):!l&&d?e=>!c.has(e)&&!s.has(Object(n.a)(e)):a.size?e=>a.has(Object(n.a)(e))?!c.has(e):o.has(e):s.size?e=>s.has(Object(n.a)(e))?o.has(e):!c.has(e):e=>o.has(e):()=>!0}},515:function(e,t,i){"use strict";i.d(t,"a",function(){return a});var n=i(12);const r=()=>Promise.all([i.e(3),i.e(52)]).then(i.bind(null,579)),a=(e,t)=>{Object(n.a)(e,"show-dialog",{dialogTag:"dialog-domain-toggler",dialogImport:r,dialogParams:t})}},830:function(e,t,i){"use strict";i.r(t);i(140);var n=i(0),r=i(152),a=i(12),o=i(151),s=i(204),c=i(514),l=i(215),d=(i(297),i(203),i(214),i(532)),p=i(355),u=i(515);i(187),i(184);function h(e){var t,i=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var n=i.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,n=new Array(t);i<t;i++)n[i]=e[i];return n}function k(e,t,i){return(k="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(n){var r=Object.getOwnPropertyDescriptor(n,t);return r.get?r.get.call(i):r.value}})(e,t,i||e)}function w(e){return(w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const _=["Alexa.EndpointHealth"],x=e=>void 0===e.should_expose||e.should_expose;!function(e,t,i,n){var r=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(n){t.forEach(function(t){var r=t.placement;if(t.kind===n&&("static"===r||"prototype"===r)){var a="static"===r?e:i;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var n=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],n=[],r={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,r)},this),e.forEach(function(e){if(!m(e))return i.push(e);var t=this.decorateElement(e,r);i.push(t.element),i.push.apply(i,t.extras),n.push.apply(n,t.finishers)},this),!t)return{elements:i,finishers:n};var a=this.decorateConstructor(i,t);return n.push.apply(n,a.finishers),a.finishers=n,a},addElementPlacement:function(e,t,i){var n=t[e.placement];if(!i&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var i=[],n=[],r=e.decorators,a=r.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,r[a])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:n,extras:i}},decorateConstructor:function(e,t){for(var i=[],n=t.length-1;n>=0;n--){var r=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[n])(r)||r);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=g(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:n,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=v(e,"finisher"),n=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:n}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=v(e,"finisher"),n=this.toElementDescriptors(e.elements);return{elements:n,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var n=(0,t[i])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(n)for(var a=0;a<n.length;a++)r=n[a](r);var o=t(function(e){r.initializeInstanceElements(e,s.elements)},i),s=r.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},n=0;n<e.length;n++){var r,a=e[n];if("method"===a.kind&&(r=t.find(i)))if(y(a.descriptor)||y(r.descriptor)){if(m(a)||m(r))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");r.descriptor=a.descriptor}else{if(m(a)){if(m(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");r.decorators=a.decorators}f(a,r)}else t.push(a)}return t}(o.d.map(h)),e);r.initializeClassElements(o.F,s.elements),r.runClassFinishers(o.F,s.finishers)}([Object(n.d)("cloud-alexa")],function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(n.h)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.h)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[Object(n.h)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[Object(n.h)()],key:"_entities",value:void 0},{kind:"field",decorators:[Object(n.h)()],key:"_entityConfigs",value:()=>({})},{kind:"field",key:"_popstateSyncAttached",value:()=>!1},{kind:"field",key:"_popstateReloadStatusAttached",value:()=>!1},{kind:"field",key:"_isInitialExposed",value:void 0},{kind:"field",key:"_getEntityFilterFunc",value:()=>Object(r.a)(e=>Object(c.a)(e.include_domains,e.include_entities,e.exclude_domains,e.exclude_entities))},{kind:"method",key:"render",value:function(){if(void 0===this._entities)return n.f` <hass-loading-screen></hass-loading-screen> `;const e=Object(c.b)(this.cloudStatus.alexa_entities),t=this._getEntityFilterFunc(this.cloudStatus.alexa_entities),i=this._isInitialExposed||new Set,r=void 0===this._isInitialExposed;let a=0;const o=[],s=[];return this._entities.forEach(c=>{const l=this.hass.states[c.entity_id],d=this._entityConfigs[c.entity_id]||{},p=e?x(d):t(c.entity_id);p&&(a++,r&&i.add(c.entity_id)),(i.has(c.entity_id)?o:s).push(n.f`
        <ha-card>
          <div class="card-content">
            <state-info
              .hass=${this.hass}
              .stateObj=${l}
              secondary-line
              @click=${this._showMoreInfo}
            >
              ${c.interfaces.filter(e=>!_.includes(e)).map(e=>e.replace("Alexa.","").replace("Controller","")).join(", ")}
            </state-info>
            <ha-switch
              .entityId=${c.entity_id}
              .disabled=${!e}
              .checked=${p}
              @change=${this._exposeChanged}
            >
              ${this.hass.localize("ui.panel.config.cloud.alexa.expose")}
            </ha-switch>
          </div>
        </ha-card>
      `)}),r&&(this._isInitialExposed=i),n.f`
      <hass-subpage header="${this.hass.localize("ui.panel.config.cloud.alexa.title")}">
        <span slot="toolbar-icon">
          ${a}${this.narrow?"":n.f` selected `}
        </span>
        ${e?n.f`
                <ha-icon-button
                  slot="toolbar-icon"
                  icon="hass:tune"
                  @click=${this._openDomainToggler}
                ></ha-icon-button>
              `:""}
        ${e?"":n.f`
                <div class="banner">
                  ${this.hass.localize("ui.panel.config.cloud.alexa.banner")}
                </div>
              `}
          ${o.length>0?n.f`
                  <h1>
                    ${this.hass.localize("ui.panel.config.cloud.alexa.exposed_entities")}
                  </h1>
                  <div class="content">${o}</div>
                `:""}
          ${s.length>0?n.f`
                  <h1>
                    ${this.hass.localize("ui.panel.config.cloud.alexa.not_exposed_entities")}
                  </h1>
                  <div class="content">${s}</div>
                `:""}
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(e){k(w(i.prototype),"firstUpdated",this).call(this,e),this._fetchData()}},{kind:"method",key:"updated",value:function(e){k(w(i.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&(this._entityConfigs=this.cloudStatus.prefs.alexa_entity_configs)}},{kind:"method",key:"_fetchData",value:async function(){const e=await Object(d.a)(this.hass);e.sort((e,t)=>{const i=this.hass.states[e.entity_id],n=this.hass.states[t.entity_id];return Object(l.b)(i?Object(s.a)(i):e.entity_id,n?Object(s.a)(n):t.entity_id)}),this._entities=e}},{kind:"method",key:"_showMoreInfo",value:function(e){const t=e.currentTarget.stateObj.entity_id;Object(a.a)(this,"hass-more-info",{entityId:t})}},{kind:"method",key:"_exposeChanged",value:async function(e){const t=e.currentTarget.entityId,i=e.target.checked;await this._updateExposed(t,i)}},{kind:"method",key:"_updateExposed",value:async function(e,t){t!==x(this._entityConfigs[e]||{})&&(await this._updateConfig(e,{should_expose:t}),this._ensureEntitySync())}},{kind:"method",key:"_updateConfig",value:async function(e,t){const i=await Object(p.i)(this.hass,e,t);this._entityConfigs=Object.assign({},this._entityConfigs,{[e]:i}),this._ensureStatusReload()}},{kind:"method",key:"_openDomainToggler",value:function(){Object(u.a)(this,{domains:this._entities.map(e=>Object(o.a)(e.entity_id)).filter((e,t,i)=>i.indexOf(e)===t),toggleDomain:(e,t)=>{this._entities.forEach(i=>{Object(o.a)(i.entity_id)===e&&this._updateExposed(i.entity_id,t)})}})}},{kind:"method",key:"_ensureStatusReload",value:function(){if(this._popstateReloadStatusAttached)return;this._popstateReloadStatusAttached=!0;const e=this.parentElement;window.addEventListener("popstate",()=>Object(a.a)(e,"ha-refresh-cloud-status"),{once:!0})}},{kind:"method",key:"_ensureEntitySync",value:function(){this._popstateSyncAttached||(this._popstateSyncAttached=!0,window.addEventListener("popstate",()=>{},{once:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      .banner {
        color: var(--primary-text-color);
        background-color: var(
          --ha-card-background,
          var(--paper-card-background-color, white)
        );
        padding: 16px 8px;
        text-align: center;
      }
      h1 {
        color: var(--primary-text-color);
        font-size: 24px;
        letter-spacing: -0.012em;
        margin-bottom: 0;
        padding: 0 8px;
      }
      .content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        grid-gap: 8px 8px;
        padding: 8px;
      }
      ha-switch {
        clear: both;
      }
      .card-content {
        padding-bottom: 12px;
      }
      state-info {
        cursor: pointer;
      }
      ha-switch {
        padding: 8px 0;
      }

      @media all and (max-width: 450px) {
        ha-card {
          max-width: 100%;
        }
      }
    `}}]}},n.a)}}]);
//# sourceMappingURL=chunk.164e471d005092847929.js.map