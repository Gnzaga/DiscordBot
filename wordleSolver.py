from random import randint


greenSquare = ":green_square:"
yellowSquare = ":yellow_square:"
blackSquare = ":white_square_button:"
wordles = dict()
usableWordles=[]
maxTries=6
def setOfWordles():
    fn=open("wordles.txt")
    lines = fn.readlines()
    for line in lines:
        wordles[line.strip()] = True

setOfWordles()
wordlescpy = wordles
for i in range(len(wordles)):
    usableWordles.append(True)

#updates wordlist, then guesses word.
def wordle():
    greenSquare = ":green_square:"
    yellowSquare = ":yellow_square:"
    blackSquare = ":white_square_button:"
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    #This function generates the row for A users valid input
    #takes in guess and answer, assumes guess is valid length and word

    def result(guess, answer):
        nonlocal alphabet
        #@alphabet = alphabet
        out = "";
        isGreen=[False,False,False,False, False]
        isYellow=[False,False,False,False, False]
        for i in range(len(guess)):
           if guess[i] == answer[i]:
            isGreen[i] = True
            
        for i in range(len(guess)):
            for j in range(len(guess)):
                if guess[i] == answer[j]:
                    if isGreen[j] == False:
                        isYellow[i] = True
                        

        for i in range(len(guess)):
            if isGreen[i]:
                out = out + greenSquare
            elif isYellow[i]:
                out = out + yellowSquare
            elif isYellow[i] == False and isGreen[i] == False:
                index = ord(guess[i]) - 97
                if index == len(alphabet)-1:
                    alphabet = alphabet[:index] + "-"
                else:
                    alphabet = alphabet[:index] + "-" + alphabet[index+1:]
                
                
                out = out + blackSquare
        return out
    #fix later to use hash table instead of search
    def getWord():
        return list(wordles)[randint(0,len(list(wordles))-1)]



    #word = res.getWordleWord();
    word = getWord()
    #word = "drops"
    print(word)
    board = []
    row = ""
    won = False
    exitGame = False
    tries = maxTries
    out = ""
    response = getWord()
    player = 'player' 
    greens = "$$$$$"
    guesses = []
    bannedIndecies = dict()
# local check function makes sure author and channel are the same
    
    print("New Game: " + player + " -> " + word)
    for i in range(0,tries):
        if i != 0:   
            response = solver(guesses, alphabet, row, tries, greens)
        if i == 0:
            guesses.append("adieu")
            response = solver(guesses, alphabet, blackSquare+blackSquare+
                blackSquare+blackSquare+blackSquare, tries, greens)
#def solver(word, alphabet, row, tries):
        row = result(response, word.lower())    
        board.append(row)
        guesses.append(response)
        if(response == word):
            won = True
            for m in board:
                #await ctx.send(m)
                out = out + m + "\n"
            if(i == 1):
                #await ctx.send("You took 1 try to guess " + word)
                out = out + player + " took 1 try to guess " + word + "\n"
            else:    
                #wait ctx.send("You took " + str(i+1) + " tries to guess " + word)
                out = out + player + " took " + str(i+1) + " tries to guess " + "**" + word + "**" + "\n"
            print(out)
            break
        elif i != tries-1:
            #print("[" + player + "]\n" + "**Usable Letters**: " + alphabet + "\n**Guess**: " + response )
            #print(row)
            print(str(i+1) + " " + player + " -> " + response)
        
        
    if won == False:
        for i in range(len(board)):
            out = out + board[i] + "\n"
            #await ctx.send(board[i])
        out = out + player + "'s word was " + "**" + word + "**"
        #await ctx.send("The word was " + word)
        print(out)
    return won

def newDict(alphabet, oldDict, guesses, greens):
    newDict = dict()
    for (key,value) in oldDict.items():
        if isValid(alphabet, key, greens) and key not in guesses:
            
            newDict[key] = value
    return newDict

def isValid(alphabet, word, greens):
    for j in range(len(word)):
        if alphabet[ord(word[j])-97] == '-' or (greens[j] != "$" and greens[j] != word[j]):
                    
            return False

    return True

def getGreens(row, word, greens):
    rawVals = row.split(":")
    vals = []
    for i in range(len(rawVals)):
        if rawVals[i] != "":
            vals.append(rawVals[i])
        
    for i in range(len(vals)):
        if vals[i] == greenSquare[1:-1]:
            greens = greens[:i] + word[i] + greens[i+1:]    

    return greens

def solver(guesses, alphabet, row, tries, greens):
    global wordlescpy


    greens = getGreens(row, guesses[-1], greens)
    
    corChar = []
    corPlcChar = ['','','','','']

    """logic -> if I know the placement of correct letters, and I know what correct letters 
    ther are, I can filter out all words that have incorrect letters, don't have correct letters,
    and then filter ones that have correct letters but don't have correct placement"""
    pre = wordlescpy
    wordlescpy = newDict(alphabet, wordlescpy, guesses, greens)
    if len(wordlescpy) == 0:
        wordlescpy = pre
    if tries == maxTries:
        out = list(wordlescpy)[randint(0,len(list(wordlescpy))-1)]

    else:
        out = list(wordlescpy)[0]
    print("Guess: " + out)
    return out
    #return list(wordles)[randint(0,len(wordles))]


#print(solver(word, alphabet, row, tries))
count = 0
for i in range(1000):
    if True:
        print(str(i)+ ": \n")
        temp = wordle()
        if temp:
            count = count + 1
        wordlescpy=wordles
        greens="$$$$$"
        """
    except Exception:
        greens="$$$$$"
        wordlescpy=wordles
        continue
        """
    greens = "$$$$$"
    wordlescpy=wordles
print(count)


