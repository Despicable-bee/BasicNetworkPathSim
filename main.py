# Standard Libs
from typing import List

# Local libs
from NetworkComponents import Link
from NetworkComponents import Node
from NetworkComponents import Packet

from NetworkPathComputer import NetworkPathComputer

from NetworkHelpers import __DEBUG_ENABLED__
from NetworkTimeblockVisualiser import PacketTimeBlocksIndex, TimeblockVisualiser

# * MAIN CLASSES ---------------------------------------------------------------

class GlobalNetwork(object):
    def __init__(self):
        # Links
        self.__L1 = Link(transmissionRate=100e6, length=240, propSpeed=2e8)
        self.__L2 = Link(transmissionRate=100e3, length=42000e3, propSpeed=3e8)
        self.__L3 = Link(transmissionRate=100e6, length=60, propSpeed=3e8)
        self.__L4 = Link(transmissionRate=500e6, length=3300e3, propSpeed=3e8)
        self.__L5 = Link(transmissionRate=200e6, length=500, propSpeed=2e8)
        self.__L6 = Link(transmissionRate=50e6, length=60, propSpeed=2e8)

        # Nodes
        self.__C = Node(processingDelay=0, name="C", links=[self.__L1])
        self.__D1 = Node(processingDelay=0, name="D1", links=[self.__L5])
        self.__S = Node(processingDelay=0, name="S", links=[self.__L6])

        # Switches
        self.__S1 = Node(processingDelay=1e-3, name='S1', 
                links=[self.__L1, self.__L2])
        self.__S2 = Node(processingDelay=2e-3, name="S2",
                links=[self.__L2, self.__L3, self.__L4])
        self.__S3 = Node(processingDelay=0.5e-3, name="S3", 
                links=[self.__L4, self.__L5])
        self.__S4 = Node(processingDelay=0.25e-3, name="S4",
                links=[self.__L3, self.__L6])
    
    # ? PUBLIC METHODS ---------------------------------------------------------

    def queueing_example(self):
        """ In event 6, how long does it take for C to receive:
        
        - the FIRST HTTP packet
        - the SECOND HTTP packet
        - the LAST HTTP packet

        CONTEXT:
        - Event 6: Server S sends the web page to to client C, segmented into
            7 packets, which includes the HTTP response plus the HTML file.
        """
        # Clear the queues before we begin
        self.__clear_queues()

        # Create the HTTP response packets (1000 bytes each)
        for i in range(0,7):
            # Add the packet to S's Queue
            packetToSend = Packet(packetSize=1000*8)
            self.__S.add_packet_to_queue(packetToSend)

        # Construct the path the packet must take
        path = [self.__S, self.__S4, self.__S2, self.__S1, self.__C]
        
        previousBlocksSteps = []

        # List to gather all the timeblocks, used for visualising the route
        tbv = TimeblockVisualiser(nodesList=path)
        counter = 0
        while len(self.__S.get_packets()) > 0:
            currentPacketTimeBlockIndex = PacketTimeBlocksIndex(counter)
            t0 = 0
            if __DEBUG_ENABLED__:
                print("\n--------- Packet {} ---------".format(counter))
            
            # Go through every node except the last one
            for i in range(0, len(path) - 1):
                # Get the current node
                currentNode = path[i]
                nextNode = path[i + 1]
                if __DEBUG_ENABLED__:
                    print(">>> Node: {}".format(currentNode.get_name()))
                # Get the next packet in the queue (if available)
                if len(currentNode.get_packets()) > 0:
                    
                    if counter > 0:
                        previousBlocks = previousBlocksSteps[i]
                    else:
                        previousBlocks = []

                    blocks = NetworkPathComputer.compute_path_step(
                            currentNode=currentNode,
                            nextNode=nextNode, 
                            previousBlocksList=previousBlocks,
                            t0=t0)

                    # Save the time block 
                    currentPacketTimeBlockIndex.add_node_pair_time_blocks_list(
                            currentNode.get_name(), blocks)

                    # Compute the new starting point
                    t0 = blocks[-1].get_stop_time()
                    if counter > 0:
                        previousBlocksSteps[i] = blocks
                    else:
                        previousBlocksSteps.append(blocks)
                    
                else:
                    continue
            counter += 1
            tbv.add_packet_blocks_index_to_record(currentPacketTimeBlockIndex)
        
        # Print out the total delay (rounded to 3 decimal places)
        counter = 0

        print("\nQuestion 8 Results " + "-" * \
                (80 - len("Question 8 Results ")) + '\n')
        for packet in self.__C.get_packets():
            print("Packet {}: {}ms".format(counter, round(packet.get_delay()*1000,3)))
            counter += 1

        # Plot the result
        tbv.visualise_timeblock()


    # ? PRIVATE METHODS --------------------------------------------------------

    def __clear_queues(self):
        self.__C.clear_queue()
        self.__S1.clear_queue()
        self.__S2.clear_queue()
        self.__S3.clear_queue()
        self.__S4.clear_queue()
        self.__D1.clear_queue()

if __name__ == '__main__':
    gn = GlobalNetwork()
    gn.queueing_example()