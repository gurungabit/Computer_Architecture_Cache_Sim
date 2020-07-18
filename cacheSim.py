import sys
import math


# this class should have valid bits (0,1) and tag. We can name it BLock for readability.
class indexBlock:
    index = None
    HM = None
    count = 0

    def __init__(self, index, HM, count):
        self.index = index
        self.HM = HM
        self.count = count


if len(sys.argv) < 9:
    print(
        "Usage", sys.argv[0], "–f <trace file name> –s <cache size in KB> –b <block size> –a <associativity> –r <replacement policy>")
    exit(0)
traceFile = ""
cacheSize = None
blockSize = None
associativity = None
replacementPolicy = None
for index, item in enumerate(sys.argv):
    if item == '-f':
        traceFile = sys.argv[index+1]
    elif item == '-s':
        cacheSize = int(sys.argv[index+1])
    elif item == '-b':
        blockSize = int(sys.argv[index+1])
    elif item == '-a':
        associativity = int(sys.argv[index+1])
    elif item == '-r':
        replacementPolicy = sys.argv[index+1]
    else:
        continue
print("Cache Simulator - CS 3853 Summer 2020 - Group 7")
print("\nTrace File:", traceFile, "\n")
print("*"*5, "Cache Input Parameters", "*"*5)
print("Cache Size:", "\t\t\t", cacheSize, "KB")
print("Block Size:", "\t\t\t", blockSize, "bytes")
print("Associativity:", "\t\t\t", associativity)
print("Replacement Policy:", "\t\t", replacementPolicy)

associativityBits = int(math.log(associativity, 2))
accessBits = int(math.log(cacheSize, 2) + 10)
offsetBits = int(math.log(blockSize, 2))
cacheIndexBits = accessBits - offsetBits - associativityBits
addressSpaceBits = 32
tagSize = addressSpaceBits - cacheIndexBits - offsetBits
totalNumRows = pow(2, cacheIndexBits)  # also can be called number of sets
# int((cacheSize*pow(2,10))/blockSize)
totalNumBlocks = totalNumRows * associativity
overHead = pow(2, tagSize) + totalNumRows
impMemorySize = cacheSize + overHead / pow(2, 10)
impMemorySizeBytes = impMemorySize * pow(2, 10)
cost = impMemorySize * 0.07
print("\n", "*"*5, "Cache Calculated Values", "*"*5, "\n")
print("Total Blocks:", "\t\t\t", totalNumBlocks)
print("Tag Size:", "\t\t\t", tagSize, "bits")
print("Index Size:", "\t\t\t", cacheIndexBits, "bits")
print("Total # Rows:", "\t\t\t", totalNumRows)
print("Overhead size:", "\t\t\t", overHead, "bytes")
print("Implementation Memory Size: \t {:.2f} KB ({:.2f} bytes)".format(
    impMemorySize, impMemorySizeBytes))
print('Cost: \t\t\t\t ${:.2f}'.format(cost))
print()
cache = {}
compulsoryMiss = 0
hit = 0
conflictMiss = 0
LRUCount = 0


def getAttributes(address, offsetBits, cacheIndexBits, tagSize):
    offset = address[-1]
    indx = int(cacheIndexBits / 4)
    index = address[-indx-1:-1]
    tag = address[0:-4]
    return(tag, index, offset)


def performCache(bytesToRead, address):
    global LRUCount
    global compulsoryMiss
    global hit
    global conflictMiss
    newAddress = int(address, 16) + int(bytesToRead, 16)
    newTag, newIndex, newOffset = getAttributes(
        hex(newAddress), offsetBits, cacheIndexBits, tagSize)
    tag, index, offset = getAttributes(
        address, offsetBits, cacheIndexBits, tagSize)
    node = indexBlock(index, 'HM', LRUCount)
    LRUCount += 1
    if not cache:
        # Instead of cache[tag], it will be cache[index]
        # Compulsory miss and set the valid bit to 1
        cache[tag] = [node]
        compulsoryMiss += 1
        return
    
    # instead it will be if index not in cache
    if tag not in cache:
        # change cache[tag] to cache[index]
        cache[tag] = [node]
        compulsoryMiss += 1
    else:
        # Change cache[tag] to cache[index]
        for indexItem in cache[tag]:
            
            # Instead of indexItem.index, it will be indexItem.tag
            
            # Change to if indexItem.tag== tag:
            if indexItem.index == index:
                indexItem.count = LRUCount
                hit += 1
                return
        if len(cache[tag]) < associativity:
            cache[tag].append(node)
            compulsoryMiss += 1
        else:
            # replacement
            cache[tag].sort(key=lambda x: x.count)
            cache[tag].pop(0)
            conflictMiss += 1
            cache[tag].append(node)
    if newIndex != index:
        node = indexBlock(newIndex, 'HM', LRUCount)
        LRUCount += 1
        if not cache:
            cache[tag] = [node]
            compulsoryMiss += 1
            return
        if tag not in cache:
            cache[tag] = [node]
            compulsoryMiss += 1
        else:
            for indexItem in cache[tag]:
                if indexItem.index == index:
                    indexItem.count = LRUCount
                    hit += 1
                    return
            if len(cache[tag]) < associativity:
                cache[tag].append(node)
                compulsoryMiss += 1
            else:
                # replacement
                cache[newTag].sort(key=lambda x: x.count)
                cache[newTag].pop(0)
                conflictMiss += 1
                cache[newTag].append(node)


def Simulation():
    try:
        with open(traceFile) as f:
            lines = f.readlines()
            numOfAddresses = 0
            bytesToRead = 0
            for line in lines:
                if line == '\n':
                    continue
                item = line.strip().split()
                if item[0] == 'dstM:':
                    if item[1] != "00000000":
                        address = item[1]
                        performCache(bytesToRead, address)
                    if item[4] != "00000000":
                        address = item[4]
                        performCache(bytesToRead, address)
                else:
                    bytesToRead = item[1][1:3]
                    address = item[2]
                    performCache(bytesToRead, address)

    except FileNotFoundError:
        print("File not found or no file was given!")
        pass


Simulation()

print("Hit", hit)
print("ConflictMiss", conflictMiss)
print("compulsoryMiss", compulsoryMiss)


#Few things I discovered
# 1. Compulsory miss should only be incremented if the tag did not match, in our code, we are incrementing the compulsory miss for every index we miss.
