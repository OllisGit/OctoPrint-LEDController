/*
 * View model for LEDController
 *
 * Author: OllisGit
 * License: AGPLv3
 */
$(function() {
    function LEDControllerViewModel(parameters) {
        var PLUGIN_ID = "LEDController"; // from setup.py plugin_identifier

        var self = this;

        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];

        self.pluginSettings = null;

        self.redLight_enabled = ko.observable();
        self.whiteLight_enabled = ko.observable();

        // Bind button-click
        self.toggleRedLight = ko.observable();
        self.onToggleRedLightEvent = function() {
            //alert("onToggleRedLightEvent");
            // toggle redlight
            $.ajax({
                url: API_BASEURL + "plugin/LEDController?toggle=redLight",
                type: "GET"
            }).done(function( data ){
                // not needed, because onDataUpdatePluginMessage is used
                //alert("server response:"+data);
            });
        }
        self.toggleRedLight.subscribe(self.onToggleRedLightEvent, self);

        self.toggleWhiteLight = ko.observable();
        self.onToggleWhiteLightEvent = function() {
            // toggle whitelight
            $.ajax({
                url: API_BASEURL + "plugin/LEDController?toggle=whiteLight",
                type: "GET"
            }).done(function( data ){
                // not needed, because onDataUpdatePluginMessage is used
                //alert("server response:"+data);
            });
        }
        self.toggleWhiteLight.subscribe(self.onToggleWhiteLightEvent, self);

        ///////////////////////////////////////////////////// START: OctoPrint Hooks

        self.onBeforeBinding = function() {
            // assign current pluginSettings
            self.pluginSettings = self.settingsViewModel.settings.plugins[PLUGIN_ID];
        }


        // Events from Server
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            /**
             * Nachricht vom Python - Script. Siehe def on_event(self, event, payload):
             */
            if (plugin != PLUGIN_ID) {
                return;
            }

            self.redLight_enabled(data.redLight_enabled);
            self.whiteLight_enabled(data.whiteLight_enabled);

            if (data.redLight_enabled == true){
                $("#redLightId").removeClass("redLightOffImage");
                $("#redLightId").addClass("redLightOnImage");
            } else {
                $("#redLightId").removeClass("redLightOnImage");
                $("#redLightId").addClass("redLightOffImage");
            }

            if (data.whiteLight_enabled == true){
                $("#whiteLightId").removeClass("whiteLightOffImage");
                $("#whiteLightId").addClass("whiteLightOnImage");
            } else {
                $("#whiteLightId").removeClass("whiteLightOnImage");
                $("#whiteLightId").addClass("whiteLightOffImage");
            }
        }


        ///////////////////////////////////////////////////// END: OctoPrint Hooks


    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: LEDControllerViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [
            "loginStateViewModel",
            "settingsViewModel",

        ],
        // Elements to bind to, e.g. #settings_plugin_LEDController, #tab_plugin_LEDController, ...
        elements: [
            document.getElementById("navbar_plugin_ledcontroller")
        ]
    });
});
