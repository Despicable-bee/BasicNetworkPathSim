# Standard Libs
from typing import List

# Third part libs
from matplotlib import pyplot as plt

# Local libs
from NetworkComponents import Node
from NetworkComponents import TimeBlock

from NetworkHelpers import __DEBUG_ENABLED__

from NetworkHelpers import TimeBlockTypes

plt.rcParams["figure.autolayout"] = True

# * AUXILIARY CLASSES ----------------------------------------------------------

class ListWrapper:
    def __init__(self, listName: str):
        self.__listName = listName
        self.__listData: List[float] = []
    
    def get_list_name(self):
        return self.__listName

    def get_list_data(self):
        return self.__listData
    
    def add_to_list_data(self, dataToAdd: float):
        self.__listData.append(dataToAdd)

class NodePairedTimeBlocksList:
    def __init__(self, nodeName: str, blocksList: List[TimeBlock]):
        self.__nodeName = nodeName
        self.__blocksList = blocksList

    def get_node_name(self):
        return self.__nodeName

    def get_blocks_list(self):
        return self.__blocksList

    def get_queue_block(self):
        if len(self.__blocksList) == 4:
            return self.__blocksList[0]
        else:
            return None
    
    def get_processing_block(self):
        if len(self.__blocksList) == 4:
            return self.__blocksList[1]
        else:
            return self.__blocksList[0]

    def get_transmission_block(self):
        if len(self.__blocksList) == 4:
            return self.__blocksList[2]
        else:
            return self.__blocksList[1]

    def get_propagation_block(self):
        if len(self.__blocksList) == 4:
            return self.__blocksList[3]
        else:
            return self.__blocksList[2]

class PacketTimeBlocksIndex:
    def __init__(self, packetNum: int):
        self.__packetNum = packetNum
        self.__nodePairsList: List[NodePairedTimeBlocksList] = []

    def add_node_pair_time_blocks_list(self, nodeName: str, 
            blocksList: List[TimeBlock]):
        self.__nodePairsList.append(
                NodePairedTimeBlocksList(
                        nodeName=nodeName,
                        blocksList=blocksList))
    
    def get_node_pair_time_blocks_list(self):
        return self.__nodePairsList

    def get_packet_num(self):
        return self.__packetNum

# * MAIN CLASS -----------------------------------------------------------------

class TimeblockVisualiser:
    def __init__(self, nodesList: List[Node]):
        self.__listIndexes: List[PacketTimeBlocksIndex] = []
        self.__nodesList: List[Node] = nodesList
    
    def add_packet_blocks_index_to_record(self, 
            blocksIndex: PacketTimeBlocksIndex):
        self.__listIndexes.append(blocksIndex)

    def visualise_timeblock(self):
        # Determine the maximum number of delay categories available
        if __DEBUG_ENABLED__:
            for index in self.__listIndexes:
                print("Packet: {}, Node pairs: {}".format(
                        index.get_packet_num(), 
                        len(index.get_node_pair_time_blocks_list())))

        listOfListWrappers: List[ListWrapper] = []

        # Create a list of in-order ListWrappers based on the node names
        for i in range(0, len(self.__nodesList) - 1):
            # Create the queue list for this node
            queueName = "{}_QUEUE".format(self.__nodesList[i].get_name())
            listOfListWrappers.append(ListWrapper(queueName))

            # Create the processing list for this node
            procName = "{}_PROC".format(self.__nodesList[i].get_name())
            listOfListWrappers.append(ListWrapper(procName))

            # Create the transmission list for this node
            transName = "{}_TRANS".format(self.__nodesList[i].get_name())
            listOfListWrappers.append(ListWrapper(transName))

            # Create the propagation list for this node
            propName = "{}_PROP".format(self.__nodesList[i].get_name())
            listOfListWrappers.append(ListWrapper(propName))

        # Get a list of all the packets
        packetsList = []
        counter = 0
        for index in self.__listIndexes:
            packetsList.append(index.get_packet_num())
            counter = 0 # Reset the counter value
            # Go through each of the packets time block lists
            for nodePair in index.get_node_pair_time_blocks_list():
                queueBlock = nodePair.get_queue_block()

                if queueBlock == None:
                    listOfListWrappers[counter].add_to_list_data(0)
                else:
                    listOfListWrappers[counter].add_to_list_data(
                            round(queueBlock.get_total_delay()*1000,3))
                
                counter += 1

                procBlock = nodePair.get_processing_block()
                listOfListWrappers[counter].add_to_list_data(
                        round(procBlock.get_total_delay()*1000,3))
                
                counter += 1

                transBlock = nodePair.get_transmission_block()
                listOfListWrappers[counter].add_to_list_data(
                        round(transBlock.get_total_delay()*1000,3))

                counter += 1

                propBlock = nodePair.get_propagation_block()
                listOfListWrappers[counter].add_to_list_data(
                        round(propBlock.get_total_delay()*1000,3))
                
                counter += 1
        
        if __DEBUG_ENABLED__:
            print("Counter value: {}".format(counter))

        # Display all the data
        graphDataList = []
        graphListNames = []
        coloursList = [
            # S
            '#ef5350',
            '#ff867c',
            '#b61827',
            '#ef5350',
            # S4
            '#ec407a',
            '#ff77a9',
            '#b4004e',
            '#eb4b7a',
            # S2
            '#ab47bc',
            '#df78ef',
            '#790e8b',
            '#ab47bc',
            # S1
            '#5c6bc0',
            '#8e99f3',
            '#26418f',
            '#5c6bc0'
            # C
        ]
        
        counter = 0
        for _ in listOfListWrappers:
            graphListNames.append(listOfListWrappers[counter]\
                        .get_list_name())
            counter += 1

        counter = 0
        fig, ax = plt.subplots()
        previousWrapper: List[float] = [0]*len(packetsList)
        for _ in listOfListWrappers:
            if counter == 0:
                barH = ax.barh(packetsList, 
                        listOfListWrappers[counter].get_list_data(),
                        color=coloursList[counter])
                ax.bar_label(barH, label_type='center')
                graphDataList.append(barH)
            else:
                barH = ax.barh(packetsList, 
                        listOfListWrappers[counter].get_list_data(), 
                        left=previousWrapper,
                        color=coloursList[counter])
                ax.bar_label(barH, label_type='center')
                graphDataList.append(barH)

            for i in range(0,len(listOfListWrappers[counter].get_list_data())):
                previousWrapper[i] += listOfListWrappers[counter]\
                        .get_list_data()[i]
            counter += 1
            
            
            
        
        if __DEBUG_ENABLED__:
            print("\nWrapper values (ms):\n")

            for wrapper in listOfListWrappers:
                print("{}: {}".format(
                        wrapper.get_list_name(), wrapper.get_list_data()))

        plt.legend(graphDataList, graphListNames)
        plt.ylabel("Packet number")
        plt.xlabel("Time (ms)")
        plt.title("Packet delays visualised")
        plt.show()
        
            


        
        

        
