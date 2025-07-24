import re # Import regex module

try:
    # Get user input for desired number of words
    num_words_to_show_str = input("Enter the number of words you would like to see - ")
    num_words_to_show = int(num_words_to_show_str)

    # Open file for reading
    # Note: 'x.txt' path might need adjustment (e.g., '../x.txt')
    with open('x.txt', 'r', encoding='utf-8') as file_to_read:
        text_content = file_to_read.read() # Read all content

    # Clean and split text into words
    cleaned_content = re.sub(r'[^A-Za-z0-9\s]', ' ', text_content)
    words_list = cleaned_content.split()

    # Count word frequencies
    word_counts_dictionary = {}
    for word in words_list:
        word_counts_dictionary[word] = word_counts_dictionary.get(word, 0) + 1

    # Sort words by frequency (descending, using lambda)
    sorted_word_counts = sorted(word_counts_dictionary.items(), key=lambda item: item[1], reverse=True)

    # Print most frequent words (up to requested number)
    print(f"{num_words_to_show} most frequent words:")
    for i in range(min(num_words_to_show, len(sorted_word_counts))):
        word, count = sorted_word_counts[i]
        print(f"{i+1}. '{word}': {count} times")

except FileNotFoundError:
    print(f"Error: The file 'x.txt' was not found. Please check its path.") # Handle file not found
except ValueError:
    print("Error: Invalid input. Please enter a whole number.") # Handle invalid input
except Exception as e:
    print(f"An unexpected error occurred: {e}") # Handle general error