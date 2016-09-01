define([
    'dojo/_base/declare',
    'dojo/text!./templates/newGreetingTemplate.html',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin'
], function(declare, _WidgetBase, _TemplatedMixin, template){

    return declare([_WidgetBase, _TemplatedMixin], {
        templateString: template,
    });
});