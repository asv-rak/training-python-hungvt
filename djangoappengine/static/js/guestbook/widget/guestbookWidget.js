define([
    'dojo/_base/declare',
    'dojo/_base/fx',
    'dojo/_base/lang',
    'dojo/dom-style',
    'dojo/mouse',
    'dojo/on',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dojo/text!./templates/myModule.html'
], function(declare, baseFx, lang, domStyle, mouse, on, _WidgetBase, _TemplatedMixin, template){

    return declare([_WidgetBase, _TemplatedMixin], {
        templateString: template,

		//template variables
		author: "No Name",
		avatar: require.toUrl("./images/defaultAvatar.png"),
		content: "No bio",
		date: "date",
		updateBy: "updater",
		baseBackgroundColor: "#fff",
        mouseBackgroundColor: "#def",

		postCreate: function () {
			var domNode = this.domNode;
			this.inherited(arguments);
			domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
			this.own(
					on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor)),
					on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor)),
					on(domNode, "click", lang.hitch(this, "_changeContent"))
			);
		},

		_changeContent: function () {
			alert(this.content);
		},

		_changeBackground: function (newColor) {
			if (this.mouseAnim) {
				this.mouseAnim.stop();
			}
			this.mouseAnim = baseFx.animateProperty({
				node: this.domNode,
				properties: {
					backgroundColor: newColor
				},
				onEnd: lang.hitch(this, function () {
					this.mouseAnim = null;
				})
			}).play();
		},

		_setAvatarAttr: function (imagePath) {
			// We only want to set it if it's a non-empty string
			if (imagePath != "") {
				// Save it on our widget instance - note that
				// we're using _set, to support anyone using
				// our widget's Watch functionality, to watch values change
				this._set("avatar", imagePath);

				// Using our avatarNode attach point, set its src value
				this.avatarNode.src = imagePath;
			}
		}
    });
});