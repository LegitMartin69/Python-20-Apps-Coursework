import re


with open("miracle_in_the_andes.txt", "r", encoding="utf-8") as file:
    book = file.read()


pattern = re.compile("\n[A-Z]{1}[^.]*[^a-zA-Z]+love[^a-zA-Z]+[^.]\n")
findings = re.findall(pattern, book)
print(findings[0])
