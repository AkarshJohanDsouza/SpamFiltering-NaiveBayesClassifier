file1 = open('nboutput.txt','r')
filetxt= file1.readlines()
actual_class ={'ham':0, 'spam': 0}
correctly_classified = {'ham':0,'spam':0}
classified_as = {'ham':0,'spam':0}
precision = {}
recall = {}

for line in filetxt:
    linearr = line.split()
    print(linearr)
    prediction = linearr[0]
    truth = linearr[-1].split('.')[-2]
    if truth not in actual_class:
        continue
    print(prediction, truth)
    actual_class[truth] +=1
    classified_as[prediction] += 1
    if prediction== truth:
        correctly_classified[truth]+=1

for flg in actual_class:
    precision[flg] = correctly_classified[flg]/ classified_as[flg]
    recall[flg] = correctly_classified[flg] / actual_class[flg]

print(precision, recall)
f1 = {'ham': 0,'spam':0}

for flg in f1:
    f1[flg] = 2 * precision[flg] * recall[flg] / (precision[flg] + recall[flg])

print(f1)

