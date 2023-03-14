import os 
import nuke

print("Inside Nuke init.py script")

# Import Script
nuke.scriptReadFile("ACES-Convert_Image_to_mov_and_more.nk")

# Get Input and Output paths
imageInputPath = os.environ["RATZ_ImageInputPath"]
imageOutputPath = os.environ["RATZ_ImageOutputPath"]

isSequence = os.environ["RATZ_IsSequence"] == "True"
isSRGB = os.environ["RATZ_IsSRGB"] == "True"

writeNodeNumber = "1"
if(isSequence):
    writeNodeNumber = "2"
if(isSequence and isSRGB):
    writeNodeNumber = "3"

# Adjust Read Node Input File
readNode = nuke.toNode("Read"+writeNodeNumber)
if(isSequence):
    # path = imageInputPath
    path = os.path.dirname(imageInputPath)
    for seq in nuke.getFileNameList(path):
        if "#" in seq:
            readNode.knob("file").fromUserText(path + "/" + seq)
            print("sequence choosen: " + seq)
else:
    readNode.knob("file").fromUserText(imageInputPath)

# Adjust Write Node Output File
writeNode = nuke.toNode("Write"+writeNodeNumber)
writeNode.knob("file").setValue(imageOutputPath)

# Set Frame Range
frameRangeFrom = 1 if not isSequence else int(os.environ["RATZ_FrameRangeFrom"])
frameRangeTo = 1 if not isSequence else int(os.environ["RATZ_FrameRangeTo"])

# Render
print("")
print("----- Start exporting -----")

nuke.execute("Write"+writeNodeNumber,frameRangeFrom,frameRangeTo)

print("")
print("----- Script Done -----")