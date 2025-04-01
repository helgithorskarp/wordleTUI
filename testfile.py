# Read all lines from the file
with open('wordBankLarge.txt', 'r') as file:
    words = file.readlines()

# Keep only words with length between 3 and 8 (inclusive)
filtered_words = [
    word for word in words
    if 3 <= len(word.strip()) <= 8
]

# Write the filtered words back to the file
with open('wordBankLarge.txt', 'w') as file:
    file.writelines(filtered_words)
