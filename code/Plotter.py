import re

def generateDicts(log_fh, totEpochs):
    currentDict = [{} for i in range(totEpochs+1)]
    runs = [0 for i in range(totEpochs+1)]
    validEpoch = False
    validTrLoss = False

    curEpoch = trLoss = valLoss = valAcc = 0
    for line in log_fh:

        if "Epoch" in line:
            if(validEpoch):
                print(curEpoch,)
                raise Exception("Invalid state1")
            curEpoch = int(re.findall(r'\d+', line)[0])
            # print(curEpoch)
            validEpoch = True
        
        if "Train loss: " in line and validEpoch:
            if(validTrLoss):
                raise Exception("Invalid state2")
            trLoss = float(re.findall(r'\d+\.\d+', line)[0])
            # print(trLoss)
            validTrLoss = True
        elif "Train loss: " in line:
            print("MERda",line)

        p = re.compile("loss: (.*) accuracy: (.*)")
        result = p.search(line)
        if result and validEpoch:
            if not validTrLoss: # bug no trline at 276
                trLoss = 2
            
            runs[curEpoch] = 1
            valLoss = float(result.group(1).replace(',', ''))
            valAcc = float(result.group(2))
            currentDict[curEpoch] = {"epoc": curEpoch, "trainLoss": trLoss, "valLoss": valLoss, "valAccuracy": valAcc}
            # print(currentDict[curEpoch])
            validEpoch = False
            validTrLoss = False
            curEpoch = trLoss = valLoss = valAcc = 0
        elif result:
            print("MERda2",line, validTrLoss, validEpoch)

    return currentDict


# importing package
import matplotlib.pyplot as plt

with open("C:\\Users\\harjo\\Workspace\\UniPD\\repo\\3d_classification\\models\\orion_ext\\trainingOnly_adam_epoc3k.txt") as f:
    totEpochs = 3000
    epochs = [i for i in range(totEpochs)]
    listNew = generateDicts(f, totEpochs)
    print(listNew[566])
    print(listNew[567])
    print(listNew[568])
    last = totEpochs
    epochs = list(map(lambda x: x["epoc"],listNew[1:last]))
    trLoss = list(map(lambda x: x["trainLoss"],listNew[1:last]))
    valLoss = list(map(lambda x: x["valLoss"],listNew[1:last]))
    valAcc = list(map(lambda x: x["valAccuracy"],listNew[1:last]))

    
    # plot lines
    fig = plt.figure(0)
    fig.canvas.set_window_title('Train/Val Losses')
    plt.title('Train/Val Losses')
    plt.subplot(2,1, 1)
    plt.plot(epochs, trLoss, label = "TrainLoss", linestyle="-")

    # plt.subplot(2,2,2)
    plt.plot(epochs, valLoss, label = "ValidationLoss", linestyle="--")
    plt.legend(loc='upper left')

    plt.subplot(3,1,3)
    plt.plot(epochs, valAcc, label = "ValAccuracy", linestyle="-")
    plt.legend(loc='upper left')
    plt.show()
    
    # TODO add a circle where the model is saved

