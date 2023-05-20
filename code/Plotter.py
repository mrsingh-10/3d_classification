import matplotlib.pyplot as plt
import re

PRINT = False

path = "C:\\Users\\harjo\\Workspace\\UniPD\\repo\\3d_classification\\models\\orion_ext\\trainingOnly_adam_epoc3k.txt"
path = "./TrainingOutput/vgnet_v3_adam_1e-02_stuck.txt"
path = "./TrainingOutput/vgnet_v3_adam_1e-03.txt"

path400 = "./TrainingOutput/vgnet_v3_adam_1e-03_400.txt"
path600 = "./TrainingOutput/vgnet_v3_adam_1e-03_600.txt"
path800 = "./TrainingOutput/vgnet_v3_adam_1e-03_800.txt"
path1000 = "./TrainingOutput/vgnet_v3_adam_1e-03_1000.txt"
path1200 = "./TrainingOutput/vgnet_v3_adam_1e-03_1200.txt"

# Val Loss goal [ORION_3k]: 0.2861 
paths = [path400, path600, path800, path1000, path1200, path]
# paths = [path]
totEpochs = 0


def generateDictsFromFile(log_fh, etimatedTotEpochs):
    currentDict = [{} for _ in range(etimatedTotEpochs+1)]
    runs = [0 for _ in range(etimatedTotEpochs+1)]
    validEpoch = False
    validTrLoss = False

    curEpoch = trLoss = valLoss = valAcc = 0
    for line in log_fh:
        if "Epoch" in line:
            if (validEpoch):
                print(curEpoch,)
                raise Exception("Invalid state1")
            curEpoch = int(re.findall(r'\d+', line)[0])
            # print(curEpoch)
            validEpoch = True

        if "Train loss: " in line and validEpoch:
            if (validTrLoss):
                raise Exception("Invalid state2")
            trLoss = float(re.findall(r'\d+\.\d+', line)[0])
            # print(trLoss)
            validTrLoss = True
        elif "Train loss: " in line:
            print("MERda", line)

        p = re.compile("loss: (.*) accuracy: (.*)")
        result = p.search(line)
        if result and validEpoch:
            if not validTrLoss:  # bug no trline at 276
                trLoss = 2

            runs[curEpoch] = 1
            valLoss = float(result.group(1).replace(',', ''))
            valAcc = float(result.group(2))
            currentDict[curEpoch] = {
                "epoc": curEpoch, "trainLoss": trLoss, "valLoss": valLoss, "valAccuracy": valAcc}
            # print(currentDict[curEpoch])
            validEpoch = False
            validTrLoss = False
            curEpoch = trLoss = valLoss = valAcc = 0
        elif result:
            print("MERda2", line, validTrLoss, validEpoch)
    return [li for li in currentDict if li]


# get all epocs from files in paths
def generateDicts(paths):
    global totEpochs
    all = []
    for p in paths:
        with open(p) as f:
            all.extend(generateDictsFromFile(f, 3000))

    # reoreder and remove duplicated [last overrided the first]
    # 1) get the totEpochs, all[-1]['epoc']) cant used for general case where paths could be unordered
    for el in all:
        totEpochs = max(totEpochs, el['epoc'])
    if PRINT:
        print("totEpocs:", totEpochs)

    # 2) remove duplicated by overriting
    if PRINT:
        print(f"before: len(all)={len(all)}")
    listNew = [{} for _ in range(totEpochs)]
    for el in all:
        listNew[el['epoc']-1] = el

    if PRINT:
        print(f"after: len(listNew)={len(listNew)}")

    listNew = [el for el in listNew if el]
    if PRINT:
        for el in listNew:
            print(el)

    return listNew

annot = ax = sc = fig = x = y = None
import numpy as np

names = np.array(list("ABCDEFGHIJKLMNO"))
def plot(listNew):
    global annot, ax, sc, fig,x ,y
    epochs = list(map(lambda x: x["epoc"], listNew))
    trLoss = list(map(lambda x: x["trainLoss"], listNew))
    valLoss = list(map(lambda x: x["valLoss"], listNew))
    valAcc = list(map(lambda x: x["valAccuracy"], listNew))

    fig = plt.figure(0)
    fig.canvas.manager.set_window_title('Train/Val Losses and Val Accuracy')
    plt.title('Train/Val Losses and Val Accuracy')
    ax = plt.subplot(2, 1, 1)
    ax.set_title('Train/Val Losses')
    ax.set_xlabel('Epochs', fontsize=10)
    ax.set_ylabel('Loss', fontsize=10)
    plt.plot(epochs, trLoss, label="TrainLoss", linestyle="-")

    # plt.subplot(2,2,2)
    plt.plot(epochs, valLoss, label="ValidationLoss",
             linestyle="--")


    # ADDING points where the model is saved
    saved = [0 for _ in range(totEpochs)]
    min = 2.5
    for el in listNew:
        if el and el['valLoss'] < min:
            min = el['valLoss']
            saved[el["epoc"]-1] = el['valLoss']

    x = list([i for i, j in zip([i+1 for i in range(totEpochs)], saved) if j != 0])
    y = list([i for i in saved if i != 0])
    sc = plt.scatter(x, y, label="Model Updated", marker=".", c="green")
    # ADDING hover to those points
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.legend(loc='upper right')

    # VALIDATION 
    ax2 = plt.subplot(3, 1, 3)
    ax2.set_title("Val Accuracy")
    ax2.set_xlabel('Epochs', fontsize=10)
    ax2.set_ylabel('Accuracy', fontsize=10)
    plt.plot(epochs, valAcc, label="ValAccuracy", linestyle="-")
    plt.legend(loc='lower right')
    plt.show()

def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    # text = "{},\n {}".format(" ".join([str(x[n]) for n in ind["ind"]]),
    #                        " ".join([str(y[n])[:7] for n in ind["ind"]]))
    text = "{}\n{}".format(str(x[ind["ind"][-1]]),str(y[ind["ind"][-1]])[:6])
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor("green")
    annot.get_bbox_patch().set_alpha(0.4)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

PLOT = True
if PLOT:
    plot(generateDicts(paths))
    