from numpy import*
# -*- coding: utf-8 -*-

def loadDataSet():
	 postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
	 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
	 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
	 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
	 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
	 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
	 classVec = [0,1,0,1,0,1]
	 return postingList,classVec




def creatVocabList(dataSet):
	vocabSet=set([])
	for document in dataSet:
		vocabSet=vocabSet|set(document)
	return list(vocabSet)
	
		





def setOfWords2Vec(vocabList,inputset):
	returnVec=[0]*len(vocabList)
	for word in inputset:
		if word in vocabList:
				returnVec[vocabList.index(word)]=1
		else:print"the word:%s is not in my Vocabulary!"% word
	return returnVec


def trainNB0(trainMatrix,trainCategory):
	numTrainDocs=len(trainMatrix)
	numWords=len(trainMatrix[0])
	PAbusive=sum(trainCategory)/float(numTrainDocs)
	p0Num=ones(numWords);p1Num=ones(numWords)
	p0Denom=2.0;p1Denom=2.0
	for i in range(numTrainDocs):
		if trainCategory[i]==1:
			p1Num+=trainMatrix[i]
			p1Denom+=sum(trainMatrix[i])
		else:
			p0Num+=trainMatrix[i]
			p0Denom+=sum(trainMatrix[i])
	p1Vect=log(p1Num/p1Denom)
	p0Vect=log(p0Num/p0Denom)
	return p0Vect,p1Vect,PAbusive


def classifyNB(vec2Classify,p0Vect,p1Vect,pClass1):
	p1=sum(vec2Classify*p1Vect)+log(pClass1)
	p0=sum(vec2Classify*p0Vect)+log(1.0-pClass1)
	if p1>p0:
		return 1
	else:
		return 0
def testingNB():
	listOPosts,listClasses=loadDataSet()
	myVocablist=creatVocabList(listOPosts)
	trainMat=[]
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocablist,postinDoc))
	p0V,p1V,pAb=trainNB0(array(trainMat),array(listClasses))
	testEntry=['love','my','dalmation']
	thisDoc=array(setOfWords2Vec(myVocablist,testEntry))
	print testEntry,'classified as"',classifyNB(thisDoc,p0V,p1V,pAb)
	testEntry=['stupid','garbage']
	thisDoc=array(setOfWords2Vec(myVocablist,testEntry))
	print testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb)

def bagOfWords2VecMN(vocabList,inputset):
	returnVec=[0]*len(vocabList)
	for word in inputset:
		if word in vocabList:
			returnVec[vocabList.index(word)]+=1
	return returnVec

def textParse(bigString):
	import re
	listOftokens=re.split(r'\W*',bigString)
	return[tok.lower() for tok in listOftokens if len(tok)>2]

def spamTest():
	docList=[];classList=[];fullText=[]
	for i in range(1,26):
		wordList=textParse(open('email/spam/%d.txt'%i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList=textParse(open('email/ham/%d.txt' %i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList=creatVocabList(docList)
	trainingSet=range(50);testSet=[]
	for i in range(10):
		randIndex=int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat=[];trainClasses=[]
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
		trainClasses.append(classList[docIndex])
		p0V,p1V,pspam=trainNB0(array(trainMat),array(trainClasses))
		errorCount=0
	for doc in testSet:
		wordVector=setOfWords2Vec(vocabList,docList[docIndex])
		if classifyNB(array(wordVector),p0V,p1V,pspam)!=classList[docIndex]:errorCount+=1
	print('the error rate is:',float(errorCount)/len(trainingSet))

def clacMostFreq(vocabList,fullText):
	import operator
	freqDict={}
	for token in vocabList:
		freqDict[token]=fullText.count(token)
	sortedFreq=sorted(freqDict.iteritems(),key=operator.itemgetter(1),reversed=True)
	return sortedFreq[:30]

def localWords(feed1,feed0):
	import feedparser
	docList=[];classList=[];fullText=[]
	minLen=min(len(feed1['entries']),len(feed0['entries']))
	for i in range(minLen):
		wordList=textParse(feed1['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList=textParse(feed0['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList=creatVocabList(docList)
	top30Words=clacMostFreq(vocabList,fullText)
	for pairW in top30Words:
		if pairW[0] in vocabList:
			vocabList.remove(pairW[0])
		trainingSet=range(2*minLen);testSet=[]
	for i in range(20):
		randIndex=int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat=[];trainClasses=[]
	for docIndex in trainingSet:	
		trainMat.append(bagOfWords2VecMN(vocabList,docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V,p1V,pspam=trainNB0(array(trainMat),array(trainClasses))
	errorCount=0
	for docIndex in testSet:
		wordVector=bagOfWords2VecMN(vocabList,docList(docIndex))
		if classifyNB(array(wordVector),p0V,p1V,pspam)!=classList[docIndex]:
			errorCount+=1
	print'the error rate is:',float(errorCount)/len(testSet)
	return vocabList,p0V,p1V

	def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0]



