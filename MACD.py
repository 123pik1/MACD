import pandas as pd

def toFloats(array):
    float_array = []
    for i in array:
        item = float(i.replace(',',''))
        float_array.append(item)
    return float_array


def alphaCalc(N):
    return 2 / (N + 1)


def EMA_element_calc(data, N, nmb_of_curr_elem):
    alpha=alphaCalc(N)
    emaNumerator = 0
    emaDenominator =0
    for j in range(0,nmb_of_curr_elem):
        emaNumerator += ((1-alpha)**j)*data[i-j]
        emaDenominator += (1-alpha)**j
    return emaNumerator/emaDenominator


def EMA_calc(data, N):
    EMAs_array = []
    for i in range(0,len(data)): #through all numbers
        emaElem =0
        if i<N: #check if actual address in array is less than N then nmb of elements equals i
            emaElem = EMA_element_calc(data, N, i)
        else: #if actual address higher or equal to N then nmb of elements equals N
            emaElem = EMA_element_calc(data, N, N)
        EMAs_array.append(emaElem)
    return EMAs_array


data_from_csv = pd.read_csv('Bitcoin-Historical-Data.csv')
data_for_calc = data_from_csv['Price']
data_for_calc = toFloats(data_for_calc)

EMA12 = EMA_calc(data_for_calc, 12)
