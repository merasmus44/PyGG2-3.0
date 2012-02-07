#!/usr/bin/env python

from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import struct
import event_serialize
import constants

class Packet(object):
    def __init__(self, sender):
        self.sequence = None
        self.acksequence = None
        self.events = []
        self.sender = sender

    def pack(self):
        packetstr = ""

        packetstr += struct.pack(">HH", self.sequence, self.acksequence)

        for event in self.events:
            packetstr += struct.pack(">B", event.eventid)
            packetstr += event.pack()

        text = open("data_sent", "w")
        text.write(packetstr)
        text.close()

        return packetstr

    def unpack(self, packetstr):
        self.events = []
        statedata = []

        self.sequence, self.acksequence = struct.unpack_from(">HH", packetstr)
        packetstr = packetstr[struct.calcsize(">HH"):]

        text = open("data", "w")
        text.write(packetstr)
        text.close()

        while packetstr:
            eventid = struct.unpack_from(">B", packetstr)[0]
            packetstr = packetstr[struct.calcsize(">B"):]

            if self.sender == "client":
                packet_event = object.__new__(event_serialize.clientevents[eventid])
            else:
                packet_event = object.__new__(event_serialize.serverevents[eventid])

            eventsize = packet_event.unpack(packetstr)
            packetstr = packetstr[eventsize:]

            # Separate states and events
            if eventid in (constants.INPUTSTATE, constants.SNAPSHOT_UPDATE, constants.FULL_UPDATE):
                statedata.append(packet_event)
            else:
                self.events.append(packet_event)

            # Append the state updates to the end of the normal event list.
            self.events += statedata
