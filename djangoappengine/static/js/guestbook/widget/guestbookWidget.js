define([
	'dojo/_base/declare',
	'dojo/request',
	'dojo/request/xhr',
	'dojo/_base/fx',
	'dojo/_base/lang',
	'dojo/dom-style',
	'dojo/mouse',
	'dojo/on',
	'dijit/_WidgetBase',
	'dijit/_TemplatedMixin',
	'dojo/text!./templates/myModule.html'
], function(declare, request, xhr, baseFx, lang, domStyle, mouse, on, _WidgetBase, _TemplatedMixin, template){

	return declare([_WidgetBase, _TemplatedMixin], {
		templateString: template,

		//template variables
		id: "no id",
		author: "No Name",
		avatar: require.toUrl("./images/defaultAvatar.png"),
		content: "No bio",
		date: "date",
		updateBy: "updater",
		baseBackgroundColor: "#fff",
		mouseBackgroundColor: "#def",
		target: "",

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

		_setIdAttr: function(id){
			this.id = id;
			this.target = lang.replace("http://localhost:8080/api/guestbook/default_guestbook/greeting/{0}", [this.id]);
		},

		_changeContent: function () {
			info = '{"greeting_content": "modified", "guestbook_name": "default_guestbook"}';

			xhr.put(this.target,{
				data: info,
				headers: {
					"X-Requested-With": null,
					"X-Http-Method-Override": "PUT",
					"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
				},
				handleAs: "text"
			}).then(function(res){
				alert("Post modified.")
			}, function(err){
				alert("Please check the input length.")
			});
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