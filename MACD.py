import matplotlib.pyplot as plt
import pandas as pd

#consts
sizeOfPlot = (16,7)


def alphaCalc(N):
    return 2 / (N + 1)

data = pd.read_csv('Data.csv')

def subArrays(arr1, arr2):
    resultArr = []
    length = len(arr1)
    if len(arr2)<length:
        length = len(arr2)
    for i in range(0, length):
        resultArr.append(arr1[i]-arr2[i])
    return resultArr
def EMA_element_calc(data, N, id_of_curr_elem):
    """
    Calculates EMA of N elements starting from data[id_of_curr_elem], goes backwards
    
    Arguments:
    data - input array
    N - number of elements
    id_of_curr_elem - id of start in input array
    """
    
    OneMinusAlpha=1-alphaCalc(N)
    emaNumerator = data[id_of_curr_elem]
    emaDenominator =1
    for i in range(1, min(N, id_of_curr_elem+1)):
        emaNumerator+=(OneMinusAlpha**i)*data[id_of_curr_elem-i]
        emaDenominator+=OneMinusAlpha**i
    return emaNumerator/emaDenominator
def EMA_calc(data, N):
    EMAs_array = []
    for i in range(0,len(data)): #through all numbers
        emaElem = EMA_element_calc(data, N, i)
        EMAs_array.append(emaElem)
    return EMAs_array
def toFloats(array):
    float_array = []
    for i in array:
        item = float(i.replace(',',''))
        float_array.append(item)
    return float_array
def intersectionPoints(MACD, SIGNAL): 
    """Finds points of intersection and return three array: intersection, buy and sell
    buy and sell are lists of tuples which containt (id, val)"""
    intersection = []
    buy = []
    sell = []
    for i in range(1, len(MACD)-1): #skip first because there is no way to analyse if it would be buy or sell
       
        if MACD[i-1] < SIGNAL[i-1] and MACD[i] > SIGNAL[i]:
            intersection.append(i) #add id in MACD array to intersection array
            buy.append((i,MACD[i]))
        elif MACD[i-1] > SIGNAL[i-1] and MACD[i] < SIGNAL[i]:
            intersection.append(i)
            sell.append((i,MACD[i]))       
    return intersection, buy, sell
def extractFromTuple(tupleArr, index):
    arrRes = []
    for i in tupleArr:
        arrRes.append(i[index])
    return arrRes
def getArrayOfIndexes(entry, indexArr):
    result = []
    for i in indexArr:
        result.append(entry[i])
    return result
data_from_csv = pd.read_csv('Data.csv')
data_for_calc = data_from_csv['Close']
data_for_calc = data_for_calc.tolist()
data_for_calc = data_for_calc[::-1]

dates = pd.to_datetime(data_from_csv['Data'], format='%Y-%m-%d')
dates=dates.tolist()
dates = dates[::-1]
EMA12 = EMA_calc(data_for_calc, 12)
EMA26 = EMA_calc(data_for_calc,26)
MACD = subArrays(EMA12,EMA26)
SIGNAL = EMA_calc(MACD,9)

intersectPoints, buyArray, sellArray = intersectionPoints(MACD, SIGNAL)

plt.figure(figsize=sizeOfPlot)
plt.plot(dates,MACD, label='MACD', color='blue') 
plt.plot(dates,SIGNAL, label='SIGNAL', color='orange')

buyPoints = getArrayOfIndexes(dates, extractFromTuple(buyArray,0))
buyValues = extractFromTuple(buyArray,1)
sellPoints = getArrayOfIndexes(dates, extractFromTuple(sellArray,0))
sellValues = extractFromTuple(sellArray,1)

plt.scatter(buyPoints, buyValues, color='green', marker='^', label='Buy', s=100)
plt.scatter(sellPoints, sellValues, color='black', marker='v', label='Sell', s = 100)

plt.legend(loc='upper right')
plt.title('MACD and SIGNAL Line')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

plt.figure(figsize=sizeOfPlot)
plt.plot(dates,data_for_calc,label='WIG20 value', color='blue')

buyPoints = [point[0] for point in buyArray]
buyValues = getArrayOfIndexes(data_for_calc,buyPoints) 
buyPoints = getArrayOfIndexes(dates, extractFromTuple(buyArray,0))
sellPoints = [point[0] for point in sellArray]
sellValues = getArrayOfIndexes(data_for_calc, sellPoints)
sellPoints = getArrayOfIndexes(dates, extractFromTuple(sellArray,0))


plt.scatter(buyPoints, buyValues, color='green', marker='^', label='Buy', s=75)
plt.scatter(sellPoints, sellValues, color='red', marker='v', label='Sell', s=75)
plt.legend(loc='upper right')

plt.title('WIG20 value')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

#plot MACD and SIGNAL for 3.2.1

plt.figure(figsize=sizeOfPlot)
plt.plot(dates,MACD, label='MACD', color='blue') 
plt.plot(dates,SIGNAL, label='SIGNAL', color='orange')

plt.xlim(pd.to_datetime('2017-01-01'),pd.to_datetime('2018-01-01'))

checkedIndex = 19

buyPoints = getArrayOfIndexes(dates, extractFromTuple(buyArray,0))
buyPoints = buyPoints[checkedIndex]
buyValues = extractFromTuple(buyArray,1)
buyValues = buyValues[checkedIndex]
sellPoints = getArrayOfIndexes(dates, extractFromTuple(sellArray,0))
sellPoints = sellPoints[checkedIndex-1]
sellValues = extractFromTuple(sellArray,1)
sellValues = sellValues[checkedIndex-1]

interPoints = getArrayOfIndexes(dates, intersectPoints)
interValues = getArrayOfIndexes(MACD, intersectPoints)

plt.scatter(interPoints, interValues, color='black', marker='.', label='intersection', s=100)
plt.scatter(buyPoints, buyValues, color='green', marker='^', label='Buy', s=100)
plt.scatter(sellPoints, sellValues, color='red', marker='v', label='Sell', s = 100)


plt.legend(loc='upper right')
plt.title('MACD and SIGNAL Line')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

#plot of prices for 3.2.1


plt.figure(figsize=sizeOfPlot)
plt.plot(dates,data_for_calc,label='WIG20 value', color='blue')

plt.xlim(pd.to_datetime('2017-01-01'),pd.to_datetime('2018-01-01'))

buyPoints = [point[0] for point in buyArray]
buyValues = getArrayOfIndexes(data_for_calc,buyPoints) 
buyPoints = getArrayOfIndexes(dates, extractFromTuple(buyArray,0))
buyPoints = buyPoints[checkedIndex]
buyValues = buyValues[checkedIndex]

sellPoints = [point[0] for point in sellArray]
sellValues = getArrayOfIndexes(data_for_calc, sellPoints)
sellPoints = getArrayOfIndexes(dates, extractFromTuple(sellArray,0))
sellPoints = sellPoints[checkedIndex-1]
sellValues = sellValues[checkedIndex-1]

interPoints = getArrayOfIndexes(dates, intersectPoints)
interValues = getArrayOfIndexes(data_for_calc, intersectPoints)

plt.scatter(interPoints, interValues, color='black', marker='.', label='intersection', s=100)
plt.scatter(buyPoints, buyValues, color='green', marker='^', label='Buy', s=100)
plt.scatter(sellPoints, sellValues, color='red', marker='v', label='Sell', s = 100)



plt.legend(loc='upper right')
plt.title('WIG20 value')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

print("Values of:")
print("buying: "+str(buyValues))
print("selling: "+str(sellValues))
print("zysk: "+str(round(sellValues-buyValues,2)))
print("Dates")
print("buying: "+str(buyPoints))
print("selling: "+str(sellPoints))

#plot MACD and SIGNAL for 3.2.2

plt.figure(figsize=sizeOfPlot)
plt.plot(dates,MACD, label='MACD', color='blue') 
plt.plot(dates,SIGNAL, label='SIGNAL', color='orange')

plt.xlim(pd.to_datetime('2017-01-01'),pd.to_datetime('2018-01-01'))

checkedIndex1 = 19
checkedIndex2 = 12

buyPoints = getArrayOfIndexes(dates, extractFromTuple(buyArray,0))
buyPoints = buyPoints[checkedIndex1]
buyValues = extractFromTuple(buyArray,1)
buyValues = buyValues[checkedIndex1]
sellPoints = getArrayOfIndexes(dates, extractFromTuple(sellArray,0))
sellPoints = sellPoints[checkedIndex2]
sellValues = extractFromTuple(sellArray,1)
sellValues = sellValues[checkedIndex2]

interPoints = getArrayOfIndexes(dates, intersectPoints)
interValues = getArrayOfIndexes(MACD, intersectPoints)

plt.scatter(interPoints, interValues, color='black', marker='.', label='intersection', s=100)
plt.scatter(buyPoints, buyValues, color='green', marker='^', label='Buy', s=100)
plt.scatter(sellPoints, sellValues, color='red', marker='v', label='Sell', s = 100)


plt.legend(loc='upper right')
plt.title('MACD and SIGNAL Line')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

#plot of prices for 3.2.2


plt.figure(figsize=sizeOfPlot)
plt.plot(dates,data_for_calc,label='WIG20 value', color='blue')

plt.xlim(pd.to_datetime('2017-01-01'),pd.to_datetime('2018-01-01'))

buyPoints = [point[0] for point in buyArray]
buyValues = getArrayOfIndexes(data_for_calc,buyPoints) 
buyPoints = getArrayOfIndexes(dates, extractFromTuple(buyArray,0))
buyPoints = buyPoints[checkedIndex1]
buyValues = buyValues[checkedIndex1]

sellPoints = [point[0] for point in sellArray]
sellValues = getArrayOfIndexes(data_for_calc, sellPoints)
sellPoints = getArrayOfIndexes(dates, extractFromTuple(sellArray,0))
sellPoints = sellPoints[checkedIndex2]
sellValues = sellValues[checkedIndex2]

interPoints = getArrayOfIndexes(dates, intersectPoints)
interValues = getArrayOfIndexes(data_for_calc, intersectPoints)

plt.scatter(interPoints, interValues, color='black', marker='.', label='intersection', s=100)
plt.scatter(buyPoints, buyValues, color='green', marker='^', label='Buy', s=100)
plt.scatter(sellPoints, sellValues, color='red', marker='v', label='Sell', s = 100)



plt.legend(loc='upper right')
plt.title('WIG20 value')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

print("Values of:")
print("buying: "+str(buyValues))
print("selling: "+str(sellValues))
print("zysk: "+str(round(sellValues-buyValues,2)))
print("Dates")
print("buying: "+str(buyPoints))
print("selling: "+str(sellPoints))


#Symulacja
simulationDays = len(data_for_calc)
sellPoints = [points[0] for points in sellArray]
buyPoints = [points[0] for points in buyArray]

PLN = 0 #starting value of account
stocks = 1000 #number of start stock actions 
isSelling =True #is next operation is operation of selling?

ops =("Sell", "Buy")
recordOfOperations = [{"PLN":PLN, "Stocks":stocks, "Operation":"Start",\
                       "Kapitał":data_for_calc[simulationDays-1]*stocks+PLN}]



for i in range(simulationDays-1, 0, -1):
    valueOfAction = data_for_calc[i]
    if isSelling and i in sellPoints:
        isSelling = False
        PLN+=round(stocks*valueOfAction,2)
        stocks =0
        PLN=round(PLN,2)
        recordOfOperations.append(\
            {"PLN":round(PLN,2), "Stocks":stocks, "Operation":ops[0],\
             "Kapitał":round(valueOfAction*stocks+PLN,2)})
    elif not isSelling and i in buyPoints:
        isSelling = True
        stocks+=int(PLN//valueOfAction)
        PLN-=stocks*valueOfAction #może nie być możliwe kupienie 
        #samych pełnych akcji
        PLN=round(PLN,2)
        recordOfOperations.append(\
            {"PLN":round(PLN,2), "Stocks":stocks, "Operation":ops[1],\
             "Kapitał":round(valueOfAction*stocks+PLN,2)})


recordInPandas = pd.DataFrame(recordOfOperations)
# Convert DataFrame to LaTeX table


recordInPandas.to_csv('simulation_result.csv', index=False)


plt.figure(figsize=sizeOfPlot)



plt.plot( recordInPandas.index, recordInPandas["Kapitał"], label='Kapitał w milionach', color='blue')
plt.legend(loc='upper right')
plt.title('Capital over Time')
plt.xlabel('Days from the start of simulation')
plt.ylabel('Capital')
plt.show()
