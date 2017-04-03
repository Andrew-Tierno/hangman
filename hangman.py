import numpy as np

#The string that denotes an unknown letter
WILD_CHARACTER = "*"
#All words in Webster's Dictionary 2nd Edition (this work is relatively old
#and new words have been created in the interim)
dictionary = open("/usr/share/dict/web2").read().lower().splitlines()
dictionary = [word.replace("-", "").replace(" ", "") for word in dictionary]

#Updates the board replacing any wild card placeholders
#with the given guess if they are correct. Returns updated list
#along with whether or not the replacement actually occured for
#score keeping purposes.
def updateBoard(guess, actualPhraseLetters, secretPhraseLetters):
    guess = guess.lower()
    correctGuess = False
    for i in range(0, len(secretPhraseLetters)):
        currWordList = secretPhraseLetters[i]
        for j in range(0, len(currWordList)):
            currLetter = currWordList[j]
            if currLetter == guess:
                actualPhraseLetters[i][j] = guess
                correctGuess = True
    return (actualPhraseLetters, correctGuess)

#Determines the probability of any letter being present in the given
#word of the secret phrase based on the length of the word and the
#known letters that have been previously guessed. Returns a probability
#function that the word is any one of a given set of letters. 
def calculateProbabilityMap(wordNum, actualPhraseLetters, alreadyGuessed):
    currWord = actualPhraseLetters[wordNum]
    dic = [dictionary[i] for i in range(0, len(dictionary)) if len(dictionary[i]) == len(currWord)]
    for i in range(0, len(currWord)):
        currLetter = currWord[i]
        if currLetter != WILD_CHARACTER:
            dic = [dic[j] for j in range(0, len(dic)) if dic[j][i] == currLetter]
    occurences = [0 for i in range(0, 26)]
    for entry in dic:
        for i in range(0, len(entry)):
            if not(entry[i] in currWord) and not(entry[i] in alreadyGuessed):
                occurences[ord(entry[i]) - ord("a")] += 1
    return [float(occurence) / sum(occurences) for occurence in occurences]

#Converts the array of array of characters into a string
#for formatting convenience. 
def stringFromCharArray(arr):
    return ' '.join([''.join(word) for word in arr])

#Whether or not the program should always choose the most likely letter
MODE = "MAX"
#or choose randomly based on the distribution calculated for the probability
#map
#MODE = "RANDOM"
#Random seems pretty terrible.

def playGame(secretPhrase):
    secretPhraseList = secretPhrase.lower().split(" ")
    secretPhraseLetters = [list(secretPhraseList[i]) for i in range(0, len(secretPhraseList))]
    actualPhraseLetters = [list(WILD_CHARACTER * len(secretPhraseList[i])) for i in range(0, len(secretPhraseList))]

    errors = 0
    alreadyGuessed = []

    for i in range(0, len(actualPhraseLetters)):
        currWord = actualPhraseLetters[i]
        while WILD_CHARACTER in currWord:
            print (stringFromCharArray(actualPhraseLetters))
            probs = calculateProbabilityMap(i, actualPhraseLetters, alreadyGuessed)
            if MODE == "MAX":
                guess = chr(probs.index(max(probs)) + ord('a'))
            elif MODE == "RANDOM":
                guess = chr(np.random.choice(26, p = probs) + ord('a'))
            print("Guessing " + guess + "...")
            update = updateBoard(guess, actualPhraseLetters, secretPhraseLetters)
            alreadyGuessed.append(guess)
            actualPhraseLetters = update[0]
            isCorrectGuess = update[1]
            if isCorrectGuess:
                print("That was correct!")
            else:
                print("That was incorrect!")
                errors += 1
            print("")
    print("Game is over and the final phrase is:")    
    print(stringFromCharArray(actualPhraseLetters))
    print("Total Errors: " + str(errors))
phrase = input("Enter a Phrase: ")
playGame(phrase)
