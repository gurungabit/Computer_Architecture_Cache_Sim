import sys
import math
if len(sys.argv) < 11:
    print(
        "Usage", sys.argv[0], "–f <trace file name> –s <cache size in KB> –b <block size> –a <associativity> –r <replacement policy>")
    exit(0)
traceFile = None
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
        pass
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
tagSize = cacheIndexBits + offsetBits
totalNumRows = pow(2, cacheIndexBits)  # also can be called number of sets
totalNumBlocks = totalNumRows * associativity
addressSpaceBits = tagSize*2
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
print("Implementation Memory Size: \t {:.2f} KB (%d bytes)".format(
    impMemorySize) % impMemorySizeBytes)
print('Cost: ${:.2f}'.format(cost))
