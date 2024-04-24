
# This data is used to test the Naive Bayes algorithm
# The first number in the list is the number of times the word appears in ham (not smap) emails, while the second number is the number of times the word appears in spam emails
hamSpamData = {
    "fortune" : [0, 375],
    "next" : [125, 0],
    "programming" : [250, 0],
    "money" : [0, 750],
    "you" : [125, 375]
}

verboseSingleProb = True

def calculateNaiveBayes(wordsCounts, emailType):
    totalHamEmails = sum(wordsCounts[word][0] for word in wordsCounts)
    totalSpamEmails = sum(wordsCounts[word][1] for word in wordsCounts)

    print("Total number of ham emails: " + str(totalHamEmails))
    print("Total number of spam emails: " + str(totalSpamEmails))

    uniqueWords = len(wordsCounts)

    print("Getting the probability of the email being " + emailType)
    # Probability is set to 1 as Naive Bayes assumes independence between the words
    probability = 1.0
    wordsProbabilities = []
    for word in wordsCounts:
        if emailType == "spam":
            wordProbability = (wordsCounts[word][1] + 1) / (totalSpamEmails + uniqueWords)
        else:
            wordProbability = (wordsCounts[word][0] + 1) / (totalHamEmails + uniqueWords)
        if verboseSingleProb : print("Probability of word '" + word + "' in " + emailType + " emails: " + str(wordProbability))
        wordsProbabilities.append(wordProbability)
        probability *= wordProbability
    
    return probability

# Test the Naive Bayes algorithm
print(calculateNaiveBayes(hamSpamData, "spam"))
print(calculateNaiveBayes(hamSpamData, "ham"))
