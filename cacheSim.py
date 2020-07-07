import sys
import math
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


def readFirstTwenty():
    try:
        with open(traceFile) as f:
            lines = f.readlines()
            count = 0
            for index, line in enumerate(lines):
                if count >= 20:
                    break
                if line == '\n' or line[0:5] == 'dstM:':
                    continue
                item = line.strip().split()
                print(hex(int(item[2], 16)),
                      "({:d})" .format(int(item[1][1:3])))
                # hexNum = int(item[2], 16)
                # num2 = int(item[2], 16)
                # sum = hexNum + num2
                # print(hex(sum))
                count += 1
    except FileNotFoundError:
        print("File not found or no file was given!")
        pass


readFirstTwenty()


# def Simuation():
#     with open(traceFile) as f:
#         lines = f.readlines()
#         for index, line in enumerate(lines):
#             if line == '\n':
#                 continue
#             item = line.strip().split()
#             if item[0] == "dstM:":
#                 if item[1] == "00000000" and item[4] == "00000000":
#                     continue
#                 else:
#                     print(lines[index-1])
#                     print(line)


# Simuation()
