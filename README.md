# LEDController

[![Version](https://img.shields.io/badge/dynamic/json.svg?color=brightgreen&label=version&url=https://api.github.com/repos/OllisGit/OctoPrint-LEDController/releases&query=$[0].name)]()
[![Released](https://img.shields.io/badge/dynamic/json.svg?color=brightgreen&label=released&url=https://api.github.com/repos/OllisGit/OctoPrint-LEDController/releases&query=$[0].published_at)]()
![GitHub Releases (by Release)](https://img.shields.io/github/downloads/OllisGit/OctoPrint-LEDController/latest/total.svg)

A OctoPrint-Plugin that sends turn on/off LEDs from the NavBar.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/OllisGit/OctoPrint-LEDController/archive/master.zip


## How it works

Two new Icons in the NavBar. One turns on/off the IR-LEDs on GPIO 23 and the other Icon toggle the white LED onn GPIO 24

The plugin is used in combination with this raspberry pi camera housing: https://www.thingiverse.com/thing:2814116

![navbar](screenshots/navbar-light_on.png "LED Icons ON")
![navbar](screenshots/navbar-light_off.png "LED Icons OFF")
