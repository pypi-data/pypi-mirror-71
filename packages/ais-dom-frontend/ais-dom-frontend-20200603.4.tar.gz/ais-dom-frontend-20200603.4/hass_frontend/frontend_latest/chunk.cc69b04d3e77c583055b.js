(self.webpackJsonp=self.webpackJsonp||[]).push([[146],{233:function(e,t,a){"use strict";a(47);var l=a(55);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML=`<dom-module id="ha-style">\n  <template>\n    <style>\n    ${l.b.cssText}\n    </style>\n  </template>\n</dom-module>`,document.head.appendChild(n.content)},748:function(e,t,a){"use strict";a.r(t);a(182);var l=a(4),n=a(31);a(158),a(233);customElements.define("ha-panel-iframe",class extends n.a{static get template(){return l.a`
      <style include="ha-style">
        iframe {
          border: 0;
          width: 100%;
          position: absolute;
          height: calc(100% - 64px);
          background-color: var(--primary-background-color);
        }
      </style>
      <app-toolbar>
        <ha-menu-button hass="[[hass]]" narrow="[[narrow]]"></ha-menu-button>
        <div main-title>[[panel.title]]</div>
      </app-toolbar>

      <iframe
        src="[[panel.config.url]]"
        sandbox="allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
      ></iframe>
    `}static get properties(){return{hass:Object,narrow:Boolean,panel:Object}}})}}]);
//# sourceMappingURL=chunk.cc69b04d3e77c583055b.js.map