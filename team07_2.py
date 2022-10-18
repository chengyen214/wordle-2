def getWords(data, scale):
    source = open(data,"r")
#     solution = list()
    firstWords = list()
    for w in source:
        ww = w.strip()
#         solution.append(ww)
        if len(ww)==scale:
            firstWords.append(ww)
    return firstWords

def getColor(guess,ans):
    color = list()
    ansAvai = [1] * 7
    for i in range(7):
        if guess[i] == ans[i]:
            color.append(1)
            ansAvai[i] = 0 
        elif guess[i].lower() == ans[i].lower():
            color.append(3)
            ansAvai[i] = 0 
        else:
            check = 1
            for j in range(7):
                if guess[i] == ans[j] and ansAvai[j] and guess[j] != ans[j]:
                    color.append(2)
                    ansAvai[j] = 0 
                    check = 0
                    break
                elif guess[i].lower() == ans[j].lower() and guess[j] != ans[j] and ansAvai[j]:
                    color.append(4)
                    ansAvai[j] = 0 
                    check = 0
                    break
            if check:
                color.append(0)
    return color

import math
def entropy(bank,prob): #prob是假設選擇的單字
    # print("entropy(bank, "+prob+" )")
    freq=[0]*2187
    for w in bank:
        sit = 0
        level = 1
        color = getColor(prob,w)
        for i in range(7):
            sit+=color[i]*level
            level*=3
        freq[sit]+=1
    Hx=0
    for i in range(2187):
        if freq[i]!=0:
            probability =freq[i] /len(bank)
            Hx-=probability*math.log(probability,2)
    return Hx

def frequenChoi(bank):
    min = 2000
    minW = bank[0]
    for w in bank:
        tmp = entropy(bank,w)
        if tmp < min:
            min = tmp
            minW = w

    return minW

def frequenChoi2(bank,color):
    abc = [[chr(i+97),0] for i in range(26)]
    for w in bank:
        for i in range(7):
            if color[i]!=1 or color[i]!=3:
                abc[ord(w[i])-97][1] += 1 
    cal = [0]*len(bank)
    minEn = 10
    minI = 0
    for i in range(len(bank)):
        for w1 in bank[i]:
            tmpFre = abc[ord(w1)-97][1] / (len(bank)*7)
            cal[i] -= tmpFre * math.log(tmpFre,2)
        if cal[i] < minEn:
            minEn = cal[i]
            minI = i
    return bank[minI]

def update2(bank,color,guess):
    guess = guess.lower()
    zerocon=[0]*7
    twocon=[0]*7
    for i in range(7):
        if color[i]==0:
            ct1=0
            for j in range(7):
                if guess[i]==guess[j] and color[j]!=0:
                    ct1+=1
            zerocon[i]=ct1
        if color[i]==2 or color[i]==4 :
            ct2=0
            for j in range(7):
                if guess[i]==guess[j] and j<i and (color[j]==2 or color[j]==4 ):
                    ct2=0
                    break
                elif guess[i]==guess[j] and color[j]==0:
                    ct2=0
                    break
                elif guess[i]==guess[j]:
                    ct2+=1
            twocon[i]=ct2
    lenght=len(bank)
    delete=[0]*lenght
    for w in range(lenght):
        for i in range(7):
            if color[i]==1 and bank[w][i]!=guess[i]:
                delete[w]=1
                break
            if color[i]==3 and bank[w][i]!=guess[i]:
                delete[w]=1
                break
            elif color[i]==0:
                if bank[w][i]==guess[i]:
                    delete[w]=1
                    break
                if zerocon[i]>0:
                    counter=0
                    for j in range(7):
                        if bank[w][j]==guess[i]:
                            counter+=1
                    if counter!=zerocon[i]:
                        delete[w]=1
                        break
                else:
                    for j in range(7):
                        if bank[w][j]==guess[i]:
                            delete[w]=1
                            break
                    
            elif color[i]==2 or color[i]==4:
                if bank[w][i] == guess[i]:
                    delete[w]=1
                    break
                if twocon[i]>0 :
                    counter2=0
                    for j in range (7):
                        if bank[w][j] == guess[i]:
                            counter2+=1
                    if counter2<twocon[i]:
                        delete[w]=1
                        break
    newbank = list()
    for w in range(lenght):
        if delete[w]==0:
            newbank.append(bank[w])
    return newbank

def uplow(guess,preGuess,color):
    Capital=[0]*26
    lowPre = preGuess.lower()
    for i in range(7):
        if (color[i]==2 and preGuess[i].isupper())or(color[i]==4 and preGuess[i].islower()):
            Capital[ord(lowPre[i])-97] += 1
    tmpStr = ""
    for i in range(7):
        if (color[i]==1 and preGuess[i].isupper()) or (color[i]==3 and preGuess[i].islower() ):
            tmpStr += guess[i].upper()
        elif Capital[ord(guess[i])-97] and color[i]!=1 and color[i]!=3:
            tmpStr += guess[i].upper()
            Capital[ord(guess[i])-97] -= 1
        else:
            tmpStr += guess[i]
    return tmpStr

import sys
dicFile = sys.argv[1]
testFile = sys.argv[2]
outputFile = sys.argv[3]

scale = 7
allWords = getWords(dicFile, scale)
test = getWords(testFile, scale)

outF = open(outputFile,"w")
# sumStep = 0
for w in test:
    outF.write(w+'\n')
    bank = allWords.copy()
    step = 0
    guess = ""
    color = [0]*7
    for ii in range(10):
        if ii == 0 :
            guess = frequenChoi2(bank,color)
        elif ii == 1 :
            preGuess = guess
            guess = frequenChoi2(bank,color)
            guess = uplow(guess,preGuess,color)
        else:
            preGuess = guess
            guess = frequenChoi(bank)
            guess = uplow(guess,preGuess,color)

        color = getColor(guess,w)
        colorStr = "\""
        for i in range(scale):
            colorStr += str(color[i])
            if i != scale - 1:
                colorStr += ","
            else:
                colorStr += "\""
#         print(guess,color,colorStr)
        outF.write(str(step+1)+"; "+guess+"; "+colorStr+'\n')
#         print(str(step+1)+"; "+guess+"; "+colorStr+'\n')
        if colorStr == "\"1,1,1,1,1,1,1\"":
            break
        bank = update2(bank,color,guess)
#         print('\n',bank)
        step += 1
    outF.write(str(step+1)+'\n')
    # sumStep += (step+1)
# outF.write('\n'+"sum step = "+str(sumStep))
outF.close()