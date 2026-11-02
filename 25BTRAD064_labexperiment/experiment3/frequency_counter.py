text = input("Enter a sentence: ").lower()
words = text.split()
frequency = {}
 
for word in words:
    # Remove common punctuation around each word.
    word = word.strip(".,!?;:\"'()[]{}")
    if word:
        frequency[word] = frequency.get(word, 0) + 1
 
print("\n--- Word Frequency ---")
if not frequency:
    print("No words were entered.")
else:
    for word, count in sorted(frequency.items()):
        print(f"{word}: {count}")
