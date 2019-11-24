# Question 3
def max_word_len(filename):
    inFile = open(filename, "r")
    outFile = open("output.txt", "w")
    readLines = inFile.readlines()
    writeLines = list()
    for line in readLines[:-1]:
        writeLines.append(str(findLengthOfLargestWordInString(line)) + "\n")
    writeLines.append(str(findLengthOfLargestWordInString(readLines[len(readLines)-1])))
    outFile.writelines(writeLines)

def findLengthOfLargestWordInString(string):
    longest = 0
    words = str.split(string, " ")
    for word in words:
        temp = word.replace(" ", "")
        temp = temp.replace("\n", "")
        if longest < len(temp):
            longest = len(temp)
    return longest


# **************************************************************
# Question 5
def k_boom(start, end, k):
    message = ""
    for i in range(start, end + 1):
        if i % int(k) == 0:
            if str(k) in str(i):
                message += " bada-boom!"
            else:
                message += " boom!"
        elif str(k) in str(i):
            message += " " + "boom-"*str(i).count(str(k))
            message = message[:-1] + "!"
        else:
            message += " " + str(i)
    return message[1:len(message)]


# **************************************************************
# Question 6
def max_div_seq(n, k):
    curSeq = ""
    maxLen = 0
    for dig in str(n):
        if int(dig) % k == 0:
            curSeq += dig
            if len(curSeq) > maxLen:
                maxLen = len(curSeq)
        else:
            curSeq = ""
    return maxLen


########
# Tester
########

def test():
    # testing Q5
    s = k_boom(797, 802, 7)
    if s != 'boom-boom! bada-boom! boom! 800 801 802':
        print("error in k_boom()")

    # testing Q6
    if max_div_seq(2330024752468, 2) != 4:
        print("error in max_div_seq()")
    if max_div_seq(1357, 2) != 0:
        print("error in max_div_seq()")

test()
