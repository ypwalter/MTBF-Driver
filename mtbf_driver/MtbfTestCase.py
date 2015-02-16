# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.apps.homescreen.app import Homescreen
from marionette.by import By


class GaiaMtbfTestCase(GaiaTestCase):

    def launch_by_touch(self, name):
        self.apps.switch_to_displayed_app()
        icon = self.marionette.find_element(By.CSS_SELECTOR, '#icons [data-identifier*=' + name + ']')
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [icon])
        # Sleep because homescreen protect touch event when scrolling
        time.sleep(1)
        icon.tap()
        self.apps.switch_to_displayed_app()

    def horizontal_launch_by_touch(
            self,
            name,
            switch_to_frame=True,
            url=None,
            launch_timeout=None):
        '''
        This function is deprecated because homescreen was changed to vertical
        '''
        homescreen = Homescreen(self.marionette)
        self.marionette.switch_to_frame()
        hs = self.marionette.find_element('css selector', '#homescreen iframe')
        self.marionette.switch_to_frame(hs)
        homescreen.go_to_next_page()

        icon = self.marionette.find_element(
            'css selector',
            'li[aria-label="' + name + '"]:not([data-type="collection"])')

        while not icon.is_displayed() and homescreen.homescreen_has_more_pages:
            homescreen.go_to_next_page()

        get_current_page = "var pageHelper = window.wrappedJSObject.GridManager.pageHelper;return pageHelper.getCurrentPageNumber() > 0;"
        while not icon.is_displayed() and self.marionette.execute_script(get_current_page):
            self.marionette.execute_script('window.wrappedJSObject.GridManager.goToPreviousPage()')
            self.wait_for_condition(lambda m: m.find_element('tag name', 'body').get_attribute('data-transitioning') != 'true')
        icon.tap()

        self.marionette.switch_to_frame()

    def cleanup_storage(self):
        pass

    def cleanup_gaia(self, full_reset=True):

        # Turn on screen
        if not self.device.is_screen_enabled:
            self.device.turn_screen_on()

        # unlock
        if self.data_layer.get_setting('lockscreen.enabled'):
            self.device.unlock()

        # kill FTU if possible
        if self.apps.displayed_app.name == None:
            pass
        elif self.apps.displayed_app.name.upper() == "FTU":
            self.apps.kill(self.apps.displayed_app)

        if full_reset:
            # disable passcode
            self.data_layer.set_setting('lockscreen.passcode-lock.code', '1111')
            self.data_layer.set_setting('lockscreen.passcode-lock.enabled', False)

            # change language back to english
            self.data_layer.set_setting("language.current", "en-US")

            # reset keyboard to default values
            self.data_layer.set_setting("keyboard.enabled-layouts",
                                        "{'app://keyboard.gaiamobile.org/manifest.webapp': {'en': True, 'number': True}}")

            # reset do not track
            self.data_layer.set_setting('privacy.donottrackheader.value', '-1')

            # don't change status of airplane mode
            # if self.data_layer.get_setting('airplaneMode.enabled'):
            #    # enable the device radio, disable airplane mode
            #    self.data_layer.set_setting('airplaneMode.enabled', False)

            # Re-set edge gestures pref to False
            self.data_layer.set_setting('edgesgesture.enabled', False)

            # disable carrier data connection
            if self.device.has_mobile_connection:
                self.data_layer.disable_cell_data()

            self.data_layer.disable_cell_roaming()

            ## TODO: Disable wifi operation since Bug 1064800
            # if self.device.has_wifi:
            #     # Bug 908553 - B2G Emulator: support wifi emulation
            #     if not self.device.is_emulator:
            #         self.data_layer.enable_wifi()
            #         self.data_layer.forget_all_networks()
            #         self.data_layer.disable_wifi()

            # don't remove contact data
            # self.data_layer.remove_all_contacts()

            # reset to home screen (dispacth event first to avoid None object in touch_home_button)
            self.device._dispatch_home_button_event()
            self.device.touch_home_button()

        # disable sound completely
        self.data_layer.set_volume(0)

        # disable auto-correction of keyboard
        self.data_layer.set_setting('keyboard.autocorrect', False)

        # restore settings from testvars
        [self.data_layer.set_setting(name, value) for name, value in self.testvars.get('settings', {}).items()]

        # restore prefs from testvars
        for name, value in self.testvars.get('prefs', {}).items():
            if type(value) is int:
                self.data_layer.set_int_pref(name, value)
            elif type(value) is bool:
                self.data_layer.set_bool_pref(name, value)
            else:
                self.data_layer.set_char_pref(name, value)

    def tearDown(self):
        time.sleep(1)
        self.device.touch_home_button()
        time.sleep(1)
        GaiaTestCase.tearDown(self)
