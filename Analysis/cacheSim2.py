import sys
import math
import random


class indexBlock:
    tag = None

    def __init__(self, tag):
        self.tag = tag


if len(sys.argv) < 9:
    print(
        "Usage", sys.argv[0], "-f <trace file name> -s <cache size in KB> -b <block size> -a <associativity> -r <replacement policy>")
    exit(0)
traceFile = ""
cacheSize = None
blockSize = None
associativity = None
replacementPolicy = None
costPerBit = 0.07
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
        if replacementPolicy != 'RND' and replacementPolicy != 'RR':
            print('Replacement policy must be RND or RR')
            exit(1)
    else:
        continue

print(cacheSize, end="\t")
print(blockSize, end= "\t")
print(associativity, end="\t")
print(replacementPolicy, end="\t")


associativityBits = int(math.log(associativity, 2))
accessBits = int(math.log(cacheSize, 2) + 10)
offsetBits = int(math.log(blockSize, 2))
cacheIndexBits = accessBits - offsetBits - associativityBits
addressSpaceBits = 32
tagSize = addressSpaceBits - cacheIndexBits - offsetBits
totalNumRows = pow(2, cacheIndexBits)  # also can be called number of sets
# int((cacheSize*pow(2,10))/blockSize)
totalNumBlocks = totalNumRows * associativity
overHead = int((totalNumRows * associativity) * (tagSize / 8) +
               (totalNumRows * associativity / 8))
impMemorySize = cacheSize + overHead / pow(2, 10)
impMemorySizeBytes = impMemorySize * pow(2, 10)

# USE COST 0.05 to match output cost
cost = impMemorySize * costPerBit
print(cost, end="\t")



def getAttributes(address, offsetBits, cacheIndexBits, tagSize):

    binary = bin(address)
    if len(binary[2:]) < addressSpaceBits:
        binary = format(int(binary, 2), '032b')
    offset = hex(int(binary[-offsetBits:], 2))
    index = hex(int(binary[-cacheIndexBits + -offsetBits:-offsetBits], 2))
    tag = hex(int(binary[:-cacheIndexBits + -offsetBits], 2))
    return tag, index, offset


def performCache(bytesToRead, address):
    global compulsoryMiss
    global hit
    global conflictMiss
    global cacheAccessCnt
    global cacheMiss
    global cycles
    global robin_index

    miss_penalty = 4 * math.ceil(blockSize / 4)

    indexes = []

    tag, index, offset = getAttributes(
        int(address, 16), offsetBits, cacheIndexBits, tagSize)

    indexes.append(index)

    newAddress = int(address, 16)
    for i in range(int(bytesToRead) - 1):
        newAddress = newAddress + 1

        newTag, newIndex, newOffset = getAttributes(
            newAddress, offsetBits, cacheIndexBits, tagSize)

        if indexes[-1] != newIndex:
            indexes.append(newIndex)

    node = indexBlock(tag)

    for i in range(len(indexes)):

        index = indexes[i]
        cacheAccessCnt += 1

        if not cache:
            cache[index] = [[node], 0]
            compulsoryMiss += 1
            cycles += miss_penalty
            continue
        if index not in cache:
            cache[index] = [[node], 0]
            compulsoryMiss += 1
            cycles += miss_penalty
        else:
            found = False
            for blockTag in cache[index][0]:
                if blockTag.tag == tag:
                    hit += 1
                    cycles += 1
                    found = True
                    break
            if found:
                continue

            cycles += miss_penalty

            if len(cache[index][0]) < associativity:
                cache[index][0].append(node)
                compulsoryMiss += 1
            else:
                # replacement
                if replacementPolicy == 'RR':
                    i = cache[index][1]
                    cache[index][1] = (cache[index][1] + 1) % associativity
                elif replacementPolicy == 'RND':
                    i = random.randint(0, len(cache[index][0])-1)

                cache[index][0][i] = node
                conflictMiss += 1


def Simulation():

    global instructionCount
    global cycles

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
                        numOfAddresses += 1
                        cycles += 1
                        performCache(4, item[1])
                    if item[4] != "00000000":
                        numOfAddresses += 1
                        cycles += 1
                        performCache(4, item[4])
                else:
                    bytesToRead = item[1][1:3]
                    numOfAddresses += 1
                    instructionCount += 1
                    cycles += 2
                    address = item[2]
                    performCache(bytesToRead, address)
            return numOfAddresses
    except FileNotFoundError:
        print("File not found or no file was given!")
        pass


cache = {}
compulsoryMiss = 0
hit = 0
conflictMiss = 0
LRUCount = 0
cacheMiss = 0
cacheAccessCnt = 0
instructionCount = 0
cycles = 0


robin_index = 0
numOfAddresses = Simulation()


hit_rate = (float(hit) / cacheAccessCnt) * 100

print(hit_rate, end="\t")
print(100 - hit_rate, end="\t")

CPI = float(cycles / instructionCount)

print(CPI, end="\t")

used_space = (compulsoryMiss * (blockSize + (tagSize + 1) / 8)) / 1024
unused_space = impMemorySize - used_space
percent_unused = (unused_space / impMemorySize) * 100.0
waste = unused_space * costPerBit

print(percent_unused, end="\t")
print(waste, end="\t")
print(totalNumBlocks - compulsoryMiss)