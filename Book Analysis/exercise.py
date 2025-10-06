import re

# Finds how many word occurrences there are in the book
def find_word(word, book):
    print(word)
    pattern = re.compile(word + "[^a-zA-Z]")
    findings = re.findall(pattern, book.lower())
    print(findings)
    matches = 0
    for i in findings:
        if word in i:
            matches += 1
    if matches == 0:
        return "The book does not contain the word \"" + word + "\""

    with open("output.txt", "w", encoding="utf-8") as file:
        for i in range(len(findings)):
            book = file.write(findings[i] + "\n")
    return matches


with open("miracle_in_the_andes.txt", "r", encoding="utf-8") as file:
    book = file.read()


# Paragraphs with love
# pattern = re.compile("[^\n]*[^a-zA-Z]+love[^\n]*")
# findings = re.findall(pattern, book)

# Titles of chapters
# pattern = re.compile("[a-zA-Z ,]+\n\n")
# findings = re.findall(pattern, book)
# findings = [item.strip("\n\n") for item in findings]

# Occurence of any word
word = input("Input a word: ")
print(find_word(word, book))

"""
print(findings)

with open("output.txt", "w", encoding="utf-8") as file:
    for i in range(len(findings)):
        book = file.write(findings[i] + "\n")
"""

