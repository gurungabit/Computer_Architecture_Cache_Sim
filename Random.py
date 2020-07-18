import sys
import math
import random


class indexBlock:
    tag = None
    HM = None
    count = 0

    def __init__(self, tag, HM, count):
        self.tag = tag
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
cacheMiss = 0


def getAttributes(address, offsetBits, cacheIndexBits, tagSize):

    binary = bin(address)
    if len(binary[2:]) < addressSpaceBits:
        binary = format(int(binary, 2), '032b')
    offset = hex(int(binary[-offsetBits:], 2))
    index = hex(int(binary[-cacheIndexBits + -offsetBits:-offsetBits], 2))
    tag = hex(int(binary[:-cacheIndexBits + -offsetBits], 2))
    return tag, index, offset


cacheAccessCnt = 0


def performCache(bytesToRead, address):
    global compulsoryMiss
    global hit
    global conflictMiss
    global cacheAccessCnt
    global cacheMiss

    indexes = []

    tag, index, offset = getAttributes(
        int(address, 16), offsetBits, cacheIndexBits, tagSize)

    indexes.append(index)

    newAddress = int(address, 16)
    for i in range(int(bytesToRead)):
        newAddress = newAddress + 1

        newTag, newIndex, newOffset = getAttributes(
            newAddress, offsetBits, cacheIndexBits, tagSize)

        if indexes[-1] != newIndex:
            indexes.append(newIndex)

    node = indexBlock(tag, 'HM', LRUCount)

    for i in range(len(indexes)):

        index = indexes[i]
        cacheAccessCnt += 1

        if not cache:
            cache[index] = [node]
            compulsoryMiss += 1
            continue
        if index not in cache:
            cache[index] = [node]
            compulsoryMiss += 1
        else:
            for blockTag in cache[index]:
                if blockTag.tag == tag:
                    hit += 1
                    continue
            if len(cache[index]) < associativity:
                cache[index].append(node)
                compulsoryMiss += 1
            else:
                # replacement
                i = random.randint(0, len(cache[index])-1)
                cache[index].pop(i)
                conflictMiss += 1
                cache[index].append(node)


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
                        numOfAddresses += 1
                        performCache("4", address)
                    if item[4] != "00000000":
                        numOfAddresses += 1
                        address = item[4]
                        performCache("4", address)
                else:
                    bytesToRead = item[1][1:3]
                    numOfAddresses += 1
                    address = item[2]
                    performCache(bytesToRead, address)
            print(numOfAddresses)
    except FileNotFoundError:
        print("File not found or no file was given!")
        pass


Simulation()

print("Cache Accesses", cacheAccessCnt)
print("Hit", hit)
print("ConflictMiss", conflictMiss)
print("compulsoryMiss", compulsoryMiss)
