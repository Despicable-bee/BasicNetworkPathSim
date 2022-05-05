# Standard libs
from typing import List

# Local libs
from NetworkComponents import Node
from NetworkComponents import TimeBlock
from NetworkComponents import Link

from NetworkHelpers import TimeBlockTypes
from NetworkHelpers import __DEBUG_ENABLED__

class NetworkPathComputer:
    def __init__(self):
        pass
    
    @staticmethod
    def compute_path_step(currentNode: Node, nextNode: Node, t0: float, 
            previousBlocksList: List[TimeBlock]):
        """ Computes a given step in the network path.

        Takes the packet at the top of the queue of the `currentNode` and
            computes all time delays associated with moving said packet
            to the `nextNode`.

        ARGS:
        - currentNode: The node the packet is currently sitting at.
        - nextNode: The node the packet wants to go to.
        - t0: The time the packet arrived in the current node.

        RETURNS:

        """
        returnBlocks: List[TimeBlock] = []
        
        currentPacket = currentNode.get_next_packet()

        queuingDelay = 0

        # Determine whether we need a queuing delay or not
        for block in previousBlocksList:
            if block.get_delay_type() == TimeBlockTypes.TRANSMISSION_DELAY:
                stopTime = block.get_stop_time()
                if stopTime > t0:
                    # Add a queuing delay to the return blocks
                    returnBlocks.append(TimeBlock(
                            delayType=TimeBlockTypes.QUEUING_DELAY,
                            startTime=t0,
                            stopTime=stopTime))

                    # Factor the queuing delay for our answers
                    queuingDelay = stopTime - t0

        
        t1 = t0 + queuingDelay

        # Add a processing delay time block
        lastProcessingDelay = currentNode.get_processing_delay()

        t2 = t1 + lastProcessingDelay

        returnBlocks.append(
                TimeBlock(delayType=TimeBlockTypes.PROCESSING_DELAY,
                        startTime=t1,
                        stopTime=t2))

        currentPacket.add_delay(lastProcessingDelay + queuingDelay)

        linkFound = False

        # Find a link to the next node
        for link1 in currentNode.get_links():
            for link2 in nextNode.get_links():
                if link1 == link2:
                    currentLink = link1
                    linkFound = True
                    break
            if linkFound:
                break
            
        if not isinstance(currentLink, Link):
            raise Exception("Couldn't find link to next " + \
                    "node CN: {} NN: {}".format(
                        currentNode.get_name(), 
                        nextNode.get_name()))
        
        # Add the transmission delay to the list of blocks

        lastTransmissionDelay = currentLink.get_transmission_delay(
                                currentPacket.get_packet_size())
        
        t3 = t2 + lastTransmissionDelay

        returnBlocks.append(
                TimeBlock(delayType=TimeBlockTypes.TRANSMISSION_DELAY,
                        startTime=t2,
                        stopTime=t3))

        currentPacket.add_delay(lastTransmissionDelay)

        # Add the propagation delay to the packet
        lastPropagationDelay = currentLink.get_propagation_delay()

        t4 = t3 + lastPropagationDelay

        currentPacket.add_delay(lastPropagationDelay)

        returnBlocks.append(
                TimeBlock(delayType=TimeBlockTypes.PROPAGATION_DELAY,
                        startTime=t3,
                        stopTime=t4))

        # Place the packet into the next node
        nextNode.add_packet_to_queue(currentPacket)
        
        # print out the steps
        if __DEBUG_ENABLED__:
            print("\nFinished Queue: {}ms, ".format(round((t1)*1000,5)), end="")
            print("Finished Processing: {}ms, ".format(
                    round((t2)*1000,5)), end="") 
            print("Finished transmission: {}ms, ".format(
                    round((t3)*1000,5)), end="")
            print("Finished Propagation: {}ms\n".format(round((t4)*1000,5)))

        return returnBlocks