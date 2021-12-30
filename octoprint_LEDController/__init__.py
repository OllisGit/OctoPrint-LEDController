# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import flask
try:
    import RPi.GPIO as GPIO
except (ModuleNotFoundError, RuntimeError):
    import Mock.GPIO as GPIO  # noqa: F401

from flask import make_response
from octoprint.events import eventManager, Events

class LEDControllerPlugin(octoprint.plugin.SettingsPlugin,
						  octoprint.plugin.AssetPlugin,
						  octoprint.plugin.SimpleApiPlugin,
						  octoprint.plugin.EventHandlerPlugin,
						  octoprint.plugin.TemplatePlugin
):

    def __init__(self):
        self._redLight_enabled = False
        self._whiteLight_enabled = False

    def initialize(self):
        self._logger.info("*******INIT 22222")
        self._redLight_enabled = self._settings.get_boolean(["redLightEnabled"])
        self._logger.info("last redLightEnabled: %s" % self._redLight_enabled)
        self._whiteLight_enabled = self._settings.get_boolean(["whiteLightEnabled"])
        self._logger.info("last whiteLightEnabled: %s" % self._whiteLight_enabled)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)

        GPIO.output(23, self._redLight_enabled)
        GPIO.output(24, self._whiteLight_enabled)

    # Event-Listener
    def on_event(self, event, payload):
        # self._logger.info("*******EVENT:"+event)
        if event == Events.CLIENT_OPENED:
            self._logger.info("*******CLIENT_OPENED")
            # Initialdaten zum Frontend senden (siehe xx.js self.onDataUpdaterPluginMessage)
            self._plugin_manager.send_plugin_message(self._identifier,
                                                     dict(redLight_enabled=self._redLight_enabled,
                                                          whiteLight_enabled=self._whiteLight_enabled)
                                                     )
            return

    def get_api_commands(self):
        return dict(enable=[],
                    disable=[],
                    abort=[])
    # GET Call
    def on_api_get(self, request):
        selectedLight = request.args.get('toggle')
        selectedLightString = '' + selectedLight
        self._logger.info("*******selectedLight:" + selectedLight)
        self._logger.info("*******selectedLightString:" + selectedLightString)
        # toogle the selectedLight
        # - get current state
        # - toogle state
        # - response state back to the ui

        # RED == GPIO: 23
        if selectedLightString == 'redLight':
            self._redLight_enabled = not self._redLight_enabled
            self._settings.set_boolean(["redLightEnabled"], self._redLight_enabled)
            GPIO.output(23, self._redLight_enabled)
            self._logger.info("*******selectedLight:" + selectedLight + " is :" + str(self._redLight_enabled))
        #
        # WHITE == GPIO: 24
        if selectedLightString == 'whiteLight':
            self._whiteLight_enabled = not self._whiteLight_enabled
            self._settings.set_boolean(["whiteLightEnabled"], self._whiteLight_enabled)
            GPIO.output(24, self._whiteLight_enabled)
            self._logger.info("*******selectedLight:" + selectedLight + " is :" + str(self._whiteLight_enabled))

        self._settings.save()
        eventManager().fire(Events.SETTINGS_UPDATED)

        self._plugin_manager.send_plugin_message(self._identifier, dict(redLight_enabled=self._redLight_enabled,
                                                                        whiteLight_enabled=self._whiteLight_enabled))
        return flask.jsonify(foo="bar")

    ##~~ SettingsPlugin mixin
    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
            redLightEnabled=False,
            whiteLightEnabled=False
        )

    ##~~ AssetPlugin mixin
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/LEDController.js"],
            "css": ["css/LEDController.css"],
            "less": ["less/LEDController.less"]
        }

    ##~~ Softwareupdate hook
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "LEDController": {
                "displayName": "LEDController Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "OllisGit",
                "repo": "OctoPrint-LEDController",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/OllisGit/OctoPrint-LEDController/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "LEDController Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = LEDControllerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
