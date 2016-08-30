define([
    'dojo/_base/declare',
    'dojo/_base/fx',
    'dojo/_base/lang',
    'dojo/dom-style',
    'dojo/mouse',
    'dojo/on',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dojo/text!./templates/newGreetingTemplate.html'
], function(declare, baseFx, lang, domStyle, mouse, on, _WidgetBase, _TemplatedMixin, template){

    return declare([_WidgetBase, _TemplatedMixin], {
        templateString: template,
    });
});