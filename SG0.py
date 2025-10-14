
#!/usr/bin/env python3

"""
Program was made using Thonny and Visual Studio Code

SG0 Program
Authors: Luke Chaney, Aaron Kofman, Caleb Jacobs
Date: 10/13/2025
Description: This program reads up to 10 text files, stores each text file into a wordlist, displays uniformed table for each file and shows how many times a specific word is in the list.
"""

from os import path
from pathlib import Path
#constant
file_extension = "txt" 
#Prompt User what this program does, return nothing.
def promptUser(): 
    print("This app reads up to 10 text files, stores each text file into a wordlist, displays uniformed table for each file and shows how many times a specific word is in the list.") 
    return 0 
 
#Prompt user to enter filename, takes in x as parameter, and returns nothing when succesful
""" Take in filename, check if it has .txt on end and if it exists in filepath and then return boolean. 
"""
def getFile():
    filename = ""
    while True:
        filename = input("Please Enter a filename, you can enter up to 10 a filenames(All must be within the same folder as the app):")
        if len(filename) == 0:
            print("Input is empty, please try again.")
            continue

        if not filename.lower().endswith(".txt"):
            print("Invalid file type. Must be a text (*.txt) file.")
            continue

        file = Path(filename).resolve()
        if not file.exists():
            print("File does not exist. Please try again.")
            continue

        return str(file)

#Get continuancy boolean value from if user wants to continue entering files.
def getContinuancy(z):
    #con = continue variable
    con = input("Would you like to continue entering Files? Please enter Yes or No:").strip().lower()
    if con == "yes" or con == "y":
        z = True
    elif con == "no" or con == "n":
        z = False
    else:
        print("That answer is not valid, please try again")
        #Recursively call the definition again and return its value
        return getContinuancy(z)
    return z
    
    
#Get Content from file and make into wordlist
def getContent(filename): 
# return a wordlist.
    wordlist = []
    endFunction = False # if true the function ends
    # things to remove before adding word to list
    removables = ["!",",",".","\"","","[","]","(",")","{","}","~","?","`"] 
    while endFunction == False:
        with open(filename,"rt") as f: # file is read (r) as text (t)
            prev_word = "" # reserved for hyphenated word of previous line
            mergePrevWord = False
            i = 0
            for line in f:
                if len(prev_word)>0:# check prev_word
                    if  line.startswith(" ") != True:
                        mergePrevWord = True#merge word from                         
                words = line.split(" ")
                for word in words: # process each word
                    # print(word)
                    endofLine = len(words) - 1
                    if word == "-": #do nothing
                        word = ""
                    else:# break down words                               
                        if (mergePrevWord == True):                            
                            word = prev_word + words[0]
                            wordlist.append(word)
                            prev_word = ""
                            mergePrevWord = False
                        else:
                            # check for hyphen
                            if word.endswith("-"):
                                # check if word is at the end of line
                                if words.index(word,endofLine) == endofLine:
                                    prev_word = word # to be merged in the next line
                                else:
                                    word = word.replace("-","")
                                    wordlist.append(word)
                            elif word.startswith("-"):
                                    word = word.replace("-","")
                                    wordlist.append(word)
                            else:
                                    wordlist.append(word)                              
        endFunction = True  
    return wordlist

def getSearchWord():
    endFunction = False # if true the function ends
    LegalCharacters = 'abcdefghijklmnopqrstuvwxyz-'
    searchWord = ""
    while endFunction == False:
        answer = input("Enter a Word to search for \n(must be all alphabet or a - with no space in between 2 words): ")
        if len(answer) > 0:
            # Check Word
            valid = True
            for char in answer: # check each character
                if LegalCharacters.find(char.lower()) > -1:
                    if char == "-":
                        cindex = answer.find("-")
                        if (cindex > 0 and cindex < (len(answer)-1)):
                            continue
                        else:
                            endFunction = False
                            break
                    else:
                        valid = True
                        
                if valid == True:
                    searchWord = answer
                    endFunction = True
                else:
                    print("Word is invalid")
                    print("word must only contain letters \n(or a hyphen in between the words with no space)")
                    endFunction = False
        else:
            print("Please enter a word to search")
            endFunction = False
    return searchWord
def countOccurrences(wordList, searchWord):
    count = 0     
    for word in wordList:
        low = word.casefold()
        if low.find(searchWord.casefold()) > -1:
            count = count + 1
    return count

def continueSearch():
    yes =  ["yes", "y"]
    no = ["no", "n"]
    valid = False
    while not valid:
        answer = input("Do you want to search for another word? Please answer with Yes or No: ").strip().lower()
        if answer in yes:
            return True
        elif answer in no:
            return False
        else:
            print("Invalid answer: must be yes or no.")

def print_file_summary(all_wordlists):
    """
    This Definition will print a well-formatted table that includes:
    - 3 columns, that show filename, total number of words in file,
    and total number of distinct words in file.
    """
    if not all_wordlists:
        print("There are no files to display")
        return
        
    #Prepare data in specific format.
    rows = []
    #Append Filename, total words, and distinct words in first row. 
    for fullpath, words in all_wordlists.items():
        FileName = Path(fullpath).name
        #t_words = total   d_words = distinct
        t_words = len(words)
        d_words = len(set(w.casefold() for w in words if len(w) > 0))
        rows.append((FileName, t_words, d_words))
    
    #Create column width
    #fn_width = filename, t_width = total, d_width = distinct_width
    fn_width = max(len(r[0]) for r in rows)
    t_width = max(len(str(r[1])) for r in rows)
    d_width = max(len(str(r[2])) for r in rows)
    
    #Create Header
    header_fn = "Filename"
    header_distinct = "Distinct"
    header_total = "TotalWords"
    fn_width = max(fn_width, len(header_fn))
    t_width = max(t_width, len(header_total))
    d_width = max(d_width, len(header_distinct))
    
    
    #Print Header
    print() #Blank Line before 
    print(f'{header_fn:>{fn_width}}  {header_total:>{t_width}}  {header_distinct:>{d_width}}')
    print('-' * (fn_width + 2 + t_width + 2 + d_width))

    #Print each row now
    for name, total_words, distinct_words in rows:
        print(f'{name:>{fn_width}}  {total_words:>{t_width}}  {distinct_words:>{d_width}}')

    print()  # blank line after table
    
    
#Main Function creates global x variable and calls definitions in order. 
def main(): 
    continueWordSearch = True
    x = False
    promptUser()
    hist_word = []
    hist_count = []
    #This List stores all File lists. 
    all_wordlists = {}
    
    while x == False:
        #Call each function to perform their own task
        z = True
        y = 1
        while(z == True and y <= 10):
            file = getFile()
            words = getContent(file) # words variable holds the words for each file
            if len(words) > 0:
                all_wordlists[file] = words #store each file separately
                y += 1
                #Call getContinuancy to check if user wants to continue entering or not
                z = getContinuancy(z)
                x = True
            else:
                print("File does not exist. Please Try again.")
                z = True
                
    #Once all files are entered, call print file def to print file summary table.            
    print_file_summary(all_wordlists)
    
    while continueWordSearch == True:
        searchWord = getSearchWord()
        # count occurrences across all files
        total_count = 0
        file_counts = {}
        for f, w in all_wordlists.items():
            c = countOccurrences(w, searchWord)
            file_counts[f] = c
            print(f'The word "{searchWord}" was found in {Path(f).name}: {c} time(s).')

        # append BEFORE asking if they want to continue
        hist_word.append(searchWord)
        hist_count.append(file_counts)

        continueWordSearch = continueSearch()
        if not continueWordSearch:
            total = len(hist_word)
            print("words found: " + str(total))
            for i in range(total):
                print(f'{hist_word[i]}: {hist_count[i]}')
            print("SG1 Program Ended")
        
 
#Call Main Definition.
if __name__ == "__main__": 
    main() 
