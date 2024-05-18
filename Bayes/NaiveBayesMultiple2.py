# COMBINATION
import pandas as pd
import itertools

# This data is used to test the Naive Bayes algorithm
hamSpamData = {
    "fortune" : [0, 375],
    "next" : [125, 0],
    "programming" : [250, 0],
    "money" : [0, 750],
    "you" : [125, 375]
}

verboseSingleProb = True
hamProb = 250
spamProb = 750
totalEmails = hamProb + spamProb
verboseIndividualProbs = False

def calculateNaiveBayes(wordsData, emailType):
    cardinality = len(wordsData)
    hamCount = sum(count[0] for count in hamSpamData.values())
    spamCount = sum(count[1] for count in hamSpamData.values())

    print("\n\nGetting the probability of the email being " + emailType)
    probability = 1.0

    wordsProbabilities = []
    for word in wordsData:
        countHam = wordsData[word][0]
        countSpam = wordsData[word][1]
        print(f"\nWORD: {word}, Count Spam: {countSpam}, Count Ham: {countHam}")

        if emailType == "ham":
            wordProbability = (1 + countHam) / (cardinality + hamCount)
        elif emailType == "spam":
            wordProbability = (1 + countSpam) / (cardinality + spamCount)
        if verboseSingleProb : print(f"Probability of word '{word}' in {emailType} emails: {str(wordProbability)}")

        wordsProbabilities.append(round(wordProbability, 3))
        probability *= wordProbability

    if emailType == "ham":
        prior = hamProb / totalEmails
    elif emailType == "spam":
        prior = spamProb / totalEmails
    
    probability *= prior

    return probability, wordsProbabilities

# Generate all possible combinations of words
words = list(hamSpamData.keys())
combinations = list(itertools.product(words, repeat=2))

# Initialize a DataFrame to store the probabilities
df = pd.DataFrame(columns=['index', '(Spam, 0)', '(Spam, 1)'])

for i, combination in enumerate(combinations):
    # Calculate the probabilities for each combination
    probHam, _ = calculateNaiveBayes({word: hamSpamData[word] for word in combination}, "ham")
    probSpam, _ = calculateNaiveBayes({word: hamSpamData[word] for word in combination}, "spam")

    # Add the probabilities to the DataFrame
    df = df._append({'index': combination, '(Spam, 0)': probHam, '(Spam, 1)': probSpam}, ignore_index=True)

print(df)

# Test the Naive Bayes algorithm
probHam, wordsProbsHam = calculateNaiveBayes(hamSpamData, "ham")
probSpam, wordsProbsSpam = calculateNaiveBayes(hamSpamData, "spam")

print(f"\n\nProbability of the email being ham: {probHam}")
print(f"Probability of the email being spam: {probSpam}")

# Create a dictionary with the results
data = {
    "probsHam" : wordsProbsHam,
    "probsSpam" : wordsProbsSpam,
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Print the DataFrame
if verboseIndividualProbs : print(df)