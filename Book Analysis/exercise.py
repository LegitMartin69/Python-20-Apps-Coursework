import re

# Change the book name to scan through a different book
# It should be a path to the file you wish to open and scan.
book_name = "miracle_in_the_andes.txt"

def find_word(word, book):
    """
    Counts how many times the word appears in the text.

    :param word: String, the word to look for
    :param book: String containing the full text read from a book file.
    :return: Number of matches, or a message if none are found.
    """
    pattern = re.compile(word.lower() + "[^a-zA-Z]")
    findings = re.findall(pattern, book.lower())

    # Prints the list of all the occurrences
    #print(findings)

    matches = 0
    for i in findings:
        if word.lower() in i:
            matches += 1
    if matches == 0:
        return "The book does not contain the word \"" + word + "\""

    # Debug code for testing
    # with open("output.txt", "w", encoding="utf-8") as file:
    #    for i in range(len(findings)):
    #        book = file.write(findings[i] + "\n")

    return matches


def chapter_titles(book):
    """
    Finds possible chapter titles in the text.
    Requires proper formating of chapters in the book to work properly

    :param book: String containing the full text read from a book file.
    :return: List of chapter title candidates.
    """
    pattern = re.compile("[a-zA-Z ,]+\n\n")
    findings = re.findall(pattern, book)
    findings = [item.strip("\n\n") for item in findings]
    return findings


def find_sentences(word, book):
    """
    Returns all sentences containing the word user enters

    :param word: String, the word to look for
    :param book: String containing the full text read from a book file.
    :return: List of sentences with 'love'.
    """
    pattern = re.compile("[A-Z]{1}[^.]*[^a-zA-Z]" + word.lower() + "[^a-zA-Z]+[^.]*")
    findings = re.findall(pattern, book)
    return findings


# Initial prompt for the user to choose which function he would like to use
function_name = input("Which function would you like to use?" +
                      "\n1: Find the occurrences of a certain word in the book." +
                      "\n2: Gets the titles of chapters" +
                      "\n3: Finds the sentences which contain the word \"love\"" +
                      "\nType in a number: ")

# Opens the book file
with open(book_name, "r", encoding="utf-8") as file:
    book_text = file.read()

# Calls the proper function
if function_name == '1':
    word = input("Input a word: ")
    print("Number of matches found: " + str(find_word(word, book_text)))
elif function_name == '2':
    print(chapter_titles(book_text))
elif function_name == '3':
    word = input("Input a word: ")
    print(find_sentences(word, book_text))
else:
    print("Invalid Input")

# Debug code for testing
"""
print(findings)

with open("output.txt", "w", encoding="utf-8") as file:
    for i in range(len(findings)):
        book = file.write(findings[i] + "\n")
"""
