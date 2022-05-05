# Standard libs
from typing import List

# Local libs
from NetworkHelpers import TimeBlockTypes

# * CLASSES --------------------------------------------------------------------

class TimeBlock(object):
    def __init__(self, delayType: TimeBlockTypes, startTime: float, 
            stopTime: float):
        
        self.__delayType = delayType
        self.__startTime = startTime
        self.__stopTime = stopTime

    def get_total_delay(self):
        """ Gets the total delay in the time block. 
        
        For instance, if this were a queue delay, we could visualise this as 
        for the following structure:

        ----------------------------------------------------
        |                   Queue Delay                    |
        ----------------------------------------------------
        ^                                                  ^
        Start time                                 Stop time
        """
        return self.__stopTime - self.__startTime

    def get_delay_type(self):
        return self.__delayType

    def get_start_time(self):
        return self.__startTime

    def get_stop_time(self):
        return self.__stopTime

class Packet(object):
    def __init__(self, packetSize: int):
        # Size of the packet in BITS
        self.__packetSize = packetSize

        self.__nodalDelay = 0.0

    def get_packet_size(self):
        """ Returns the size of the packet in bits. """
        return self.__packetSize

    def get_delay(self):
        """ Gets the delay () """
        return self.__nodalDelay

    def add_delay(self, timeToAdd: float):
        """ Adds a delay to the packet (part of a cumulative total). 
        
        ARGS:
        - timeToAdd: The time to add (you can use either seconds or 
                milliseconds, but the standard is milliseconds).
        """
        self.__nodalDelay += timeToAdd

class Link(object):
    def __init__(self, transmissionRate: float, length: float, 
            propSpeed: float):
        """ Object representing a link between two nodes. """

        # The transmission rate (bits / second)
        self.__transmissionRate = transmissionRate
        
        # Length of the link (metres)
        self.__length = length

        # Propagation speed of the link (in metres / second)
        self.__propSpeed = propSpeed

    def get_transmission_delay(self, packetSize: float):
        """ Returns the amount of time to transmit a number of bits through 
                the link. """
        return packetSize / self.__transmissionRate

    def get_propagation_delay(self):
        """ Returns the propagation delay of the link """
        return self.__length / self.__propSpeed

class Node(object):
    def __init__(self, processingDelay: float, name: str, links: List[Link]):
        """ Object representing a node that comprises a network. """
        
        # The processing delay (seconds)
        self.__procDelay = processingDelay

        # The queue for all the packets
        self.__queue: List[Packet] = []

        # Name of the next node in the list
        self.__name = name

        # Links available to this node
        self.__links: List[Link] = links

    def get_name(self):
        return self.__name

    def get_links(self):
        """ Returns the list of available links for this node. 
        
        Use this to verify if a particular hop in a route can actually be 
            facilitated.
        """
        return self.__links

    def get_processing_delay(self):
        return self.__procDelay
    
    def add_packet_to_queue(self, packetToAdd: Packet):
        self.__queue.append(packetToAdd)

    def get_next_packet(self):
        """ Gets the next packet in the queue. 
        
        NOTE: This operation will `pop` the packet off the queue, so be mindful.
        """
        return self.__queue.pop(0)

    def get_packets(self):
        """ Returns the current list of packets waiting in the queue."""
        return self.__queue

    def clear_queue(self):
        """ Resets the queue (removes all packets waiting to be processed). """
        self.__queue = []