# -*- coding:utf-8 -*-

import sys
import math


class Node:
    def __init__(self, word):
        self.bestScore = 0.0
        self.bestPreNode = None
        self.len = len(word)
        self.word = word


class BiLM:
    def __init__(self, WordDicFile, biLMFile):
        self.wordNum = 0
        self.wordIDTable = {}
        self.unigramProb = []
        self.bigramProb = []
        self.unknownWordProb = 1.0

        # load WordIDTable
        infile = open(WordDicFile, 'r', encoding='gbk')
        sline = infile.readline().strip()
        self.maxWordLen = 1
        while len(sline) > 0:
            # sline = sline.decode("gb2312")
            items = sline.split(' ')
            if len(items) != 2:
                print("Lexicon format error!")
                sline = infile.readline().strip()
                continue
            self.wordIDTable[items[0]] = int(items[1])
            if len(items[0]) > self.maxWordLen:
                self.maxWordLen = len(items[0])
            sline = infile.readline().strip()
        infile.close()
        infile = open(biLMFile, 'r')
        sline = infile.readline().strip()
        items = sline.split(' ')
        if len(items) == 2:  # the first line
            self.wordNum = int(items[0])
        else:
            print("Bad format found in LM file!")
            sys.exit()
        sline = infile.readline().strip()

        # initialization unigramProb bigramProb
        # load unigramProb bigramProb
        lenWordIDTable = len(self.wordIDTable)
        self.unigramProb = [0.0 for _ in range(lenWordIDTable + 1)]
        self.bigramProb = [{} for _ in range(lenWordIDTable + 1)]
        # for i in range(len(self.wordIDTable)):
        #     self.unigramProb.append(0.0)
        #     self.bigramProb.append({})
        # self.unigramProb.append(0.0)
        # self.bigramProb.append({})

        wid = 1
        while len(sline) > 0:
            items = sline.split(' ')
            # self.unigramProb[wid] = float(items[1])
            self.unigramProb[wid] = float(items[0])
            i = 2
            while i < len(items):
                self.bigramProb[wid][int(items[i])] = float(items[i + 1])
                i += 2
            sline = infile.readline().strip()
            wid += 1
        infile.close()
        print(len(self.wordIDTable), "words loaded")

    def GetScoreBack(self, word1, word2):
        wid1 = -1
        wid2 = -1
        # if word1 not in self.wordIDTable:
        #     return self.unknownWordProb
        # wid1 = self.wordIDTable[word1]
        # if word2 not in self.wordIDTable:
        #     return self.unigramProb[wid1]

        if (word1 is not '' and word1 not in self.wordIDTable.keys())\
                or word2 not in self.wordIDTable.keys():
            print("word1 or word2 should be in wordIDTable. word1: %s, word2: %s" % (word1, word2))
            sys.exit()
        wid2 = self.wordIDTable[word2]
        if wid2 not in self.bigramProb[wid1]:
            return self.unigramProb[wid1]
        return self.bigramProb[wid1][wid2]

    def GetScore(self, word1, word2):
        # 如果preNode 不在词典中，比如" "，那么得分为0
        if word1 not in self.wordIDTable:
            # unknownWordProb = 1, log(unknownWordProb) = 0
            return self.unknownWordProb
        wid1 = self.wordIDTable[word1]  # 得到 word1 的id

        # 如果currentNode 不在词典中，则得分为preNode 的一元概率
        if word2 not in self.wordIDTable:
            return self.unigramProb[wid1]
        wid2 = self.wordIDTable[word2]  # 得到 word2 的id

        # 如果currentNode 在词典中，但没在wid1后面出现过，则得分为preNode 的一元概率,
        # 否则返回wid2 出现在wid1后面的概率
        if wid2 not in self.bigramProb[wid1]:
            return self.unigramProb[wid1]
        return self.bigramProb[wid1][wid2]


def CreateGraph(s):
    # initializatioon WordGraph
    WordGraph = [[] for _ in range(len(s) + 2)]  # +2 is start and end Node
    WordGraph[0] = [Node("")]  # start Node
    WordGraph[-1] = [Node("")]  # end Node
    # WordGraph = []
    #
    # # Start Node
    # newNode = Node("")
    # newNodeList = []
    # newNodeList.append(newNode)
    # WordGraph.append(newNodeList)
    #
    # for i in range(len(s)):
    #     WordGraph.append([])
    #
    # # End Node
    # newNode = Node(" ")
    # newNodeList = []
    # newNodeList.append(newNode)
    # WordGraph.append(newNodeList)

    # Other nodes
    for i in range(len(s)):
        j = myBiLM.maxWordLen
        if i + j > len(s):
            j = len(s) - i
        while j > 0:
            if s[i:i + j] in myBiLM.wordIDTable:
                newNode = Node(s[i:i + j])
                WordGraph[i + j].append(newNode)
            j -= 1
        if len(WordGraph[i + 1]) < 1:  # why?
            print("Unknown character found!", i, s[i])
            sys.exit()
    return WordGraph


def ViterbiSearch(WordGraph):
    # for al in WordGraph:
    # print "==="
    # for a in al:
    # print a.word
    # print "-"
    # print len(WordGraph)
    # sys.exit()
    # 此算法是石可以改进，得到level 的 bestScore即可，bestNode即可？不行。有可能后边的拖累前面的bestNode



    for i in range(len(WordGraph) - 1):
        for curNode in WordGraph[i + 1]:
            if curNode.len == 0:
                preLevel = i
            else:
                preLevel = i + 1 - curNode.len  # the level of the previous word. eg"南"，"南京市"的前一个leval为0，"市长"的前一个level为2
            if preLevel < 0:
                print("running error!")
                sys.exit()
            preNode = WordGraph[preLevel][0]
            score = myBiLM.GetScore(preNode.word, curNode.word)
            score = preNode.bestScore + math.log(score)
            maxScore = score
            curNode.bestScore = score
            curNode.bestPreNode = preNode
            for j in range(1, len(WordGraph[preLevel])):
                preNode = WordGraph[preLevel][j]
                score = myBiLM.GetScore(preNode.word, curNode.word)
                score = preNode.bestScore + math.log(score)
                if score > maxScore:
                    curNode.bestScore = score
                    curNode.bestPreNode = preNode
                    maxScore = score


def BackSearch(WordGraph):
    resultList = []
    curNode = WordGraph[len(WordGraph) - 1][0].bestPreNode
    while curNode.bestPreNode != None:
        resultList.insert(0, curNode.word)
        curNode = curNode.bestPreNode
    return resultList


WordDicFile = "./WordDic.rm.txt"
BiLMFile = "./BiModel.rm.txt"
myBiLM = BiLM(WordDicFile, BiLMFile)

inputStr = u"南京市长江大桥"
# inputStr = u"广州本田雅阁汽车"
# inputStr = u"北京大学生活动中心"

# inputStr = u"欢迎大家跟火哥学算法"

WordGraph = CreateGraph(inputStr)

for NodeList in WordGraph:
    for Node in NodeList:
        print("CurNode Word: ", Node.word)

ViterbiSearch(WordGraph)
resultList = BackSearch(WordGraph)
for word in resultList:
    print(word, '')
