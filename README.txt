
# the first word-breaking method
# hmm

Step 1.
    # convert token to id
    python CreateLexicon.py
实现如下功能：
    # 输入的分好词的文件 RenMinData.txt
    rawDataFile = "./RenMinData.txt"
    # 输出 将token转变为id RenMinData.id.txt
    idDataFile = "./RenMinData.id.txt"
    # 输出 将token 对应的id 存入到文件 WordDic.rm.txt
    wordDicFile = "./WordDic.rm.txt"

Step 2.
    # gen lang model
    python BiLMTrain.py

Step 3.
    # viterbi
    python ViterbiCWS.py

------------- 

# the second word-breaking method
# length match

Step 1.
    # dict search
    python BMM.py

