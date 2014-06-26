# -*- coding: iso-8859-15 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.clock.app import Clock
from fysom import Fysom

class TestKeyboard(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        # TODO: if clock was launched, kill it.
        self.clock = Clock(self.marionette)
        self.clock.launch()

        # prepare a state list and maximum number
        self.maximum = random.randint(10,20)
        self.record = []
        self.current_step = -99

    # 0 actions
    def onswitch(e):
        print "tap the Timer button"

    # 2 actions
    def onstart(e):
        if current_step == -99:
            step = random.randint(1,2)
            self.record.append(step)
            

    def test_timer_fsm(self):
        # simple test here
        self.fsm = Fysom({ 'initial': 'Alarm',
                           'events': [
                               {'name': 'switch', 'src': 'Alarm',     'dst': 'Timer'},
                               {'name': 'start',  'src': 'Timer',     'dst': 'Countdown'},
                               {'name': 'cancel', 'src': 'Countdown', 'dst': 'Timer'},
                               {'name': 'pause',  'src': 'Countdown', 'dst': 'Freeze'},
                               {'name': 'resume', 'src': 'Freeze',    'dst': 'Countdown'},
                               {'name': 'cancel', 'src': 'Freeze',    'dst': 'Timer'},
                               {'name': 'timeup', 'src': 'Countdown', 'dst': 'Alarm'},
                               {'name': 'stop',   'src': 'Alarm',     'dst': 'Timer'},
                               {'name': 'end',    'src': '*',         'dst': 'Exit'}],
                            'callbacks': {
                               'onswitch': onswitch,
                               'onstart':  onstart,
                               'oncancel': oncancel,
                               'onpause':  onpause,
                               'onresume': onresume,
                               'ontimeup': ontimeup,
                               'onstop':   onstop }})
	
	while True:
            self.maximum = self.maximum - 1
            print "Current status: " + fsm.current
            if self.maximum == 0:
                self.record.append(-1)
                break;
            

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
