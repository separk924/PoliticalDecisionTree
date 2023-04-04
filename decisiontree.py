import math

def createTuning():
    tuningFile = open("tuning.txt", 'w')
    
    with open("data.txt", 'r') as file:
        count = 0
        Lines = file.readlines()
        with open ("data.txt", 'w') as file:
            for line in Lines:
                num = count % 4
                if num == 0:
                    tuningFile.write(line)
                else:
                    file.write(line)
                count += 1
       
createTuning() 