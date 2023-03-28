import math

def createTrainTest():
    trainFile = open("training.txt", 'w')
    testFile = open("testing.txt", 'w')
    
    with open("data.txt", 'r') as file:
        count = 0
        Lines = file.readlines()
        lineNum = len(Lines)
        limit = math.floor(lineNum * 2/3)
        for line in Lines:
            if count >= limit:
                testFile.write(line)
            else:
                trainFile.write(line)
            count += 1

def createTuning():
    tuningFile = open("tuning.txt", 'w')
    
    with open("training.txt", 'r') as file:
        count = 0
        Lines = file.readlines()
        with open ("training.txt", 'w') as file:
            for line in Lines:
                num = count % 4
                if num == 0:
                    tuningFile.write(line)
                else:
                    file.write(line)
                count += 1
       
# createTrainTest()
createTuning() 