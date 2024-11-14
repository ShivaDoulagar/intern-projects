
# defined class
class Words:
    # defined method to calculate the number of words
    def no_of_words(self,para):
        try:
            # split to convert the given string into list
            para = para.split(' ')
            if para == []:
                # if no input is given
                return "Invalid Input! Enter paragraph."
            else:
                # returning the length of string
                return len(para)
        # if any exception occurs
        except Exception as e:
            return e
        

# defined main class  
if __name__ == "__main__":
    # Initialize object
    words = Words()
    # taking input from user
    given_input = input("Enter the paragraph to find the number of words: ")
    # printing the answer
    print(f"\n\nThe number of words in Given paragraph is:{words.no_of_words(given_input)}\n\n")