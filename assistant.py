from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
file_path = "scanner.py"
with open(file_path, "r") as f:
    code_text = f.read()

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are an extremely well researched expert in scansion of Latin poetry in Dactylic Hexameter. You also understand complex Python algorithms"},
            {"role": "user", "content": f"How would you describe the approach this program takes to algorithmically scanning latin poetry?: {code_text}"},
        ],
        temperature=0,
        #response_format={"type": "json_object"
    )
    

    print(response.choices[0].message.content.strip())
except Exception as e:
    print(f"Error: {e}")
    
"""Your Python code for scanning Latin poetry in dactylic hexameter is quite extensive and complex. Here are several suggestions for improving the code, focusing on readability, maintainability, and performance:

### 1. **Modularization and Function Decomposition**
The code is quite long and contains many nested functions. Consider breaking it down into smaller, more manageable functions. Each function should ideally perform a single task. This will make the code easier to read and maintain.

### 2. **Use of Classes**
Since you mentioned using classes, consider encapsulating related functions and data into classes. For example, you could create a `Scansion` class that holds the state of the scan, reasons, and methods for processing the lines.

### 3. **Avoid Global Variables**
Global variables can lead to code that is hard to understand and maintain. Instead, pass variables as parameters to functions or use class attributes if you implement a class.

### 4. **Use of Constants**
Define constants for strings like vowels, diphthongs, and other repeated values. This will make it easier to change them in one place if needed.

```python
VOWELS = "aeiouyAEIOUYāēīōūĀĒĪŌŪ"
DIPHTHONGS = ["ae", "au", "ei", "eu", "oe", "ai", "oi", "ou"]
```

### 5. **Improve Readability**
Use more descriptive variable names and add comments to explain complex logic. This will help others (and your future self) understand the code better.

### 6. **Error Handling**
Add error handling to manage unexpected inputs or states. This will make your code more robust.

### 7. **Use of List Comprehensions**
Wherever possible, use list comprehensions for cleaner and more Pythonic code.

### 8. **Optimize Logic**
Some of the logic can be simplified. For example, the checks for elisions and diphthongs can be consolidated into helper functions.

### 9. **Testing and Validation**
Implement unit tests to validate the functionality of your code. This will help ensure that changes do not introduce new bugs.

### 10. **Performance Considerations**
If performance becomes an issue, consider profiling your code to identify bottlenecks. Optimize those sections as needed.

### Example Refactor
Here’s a small example of how you might start refactoring part of your code:

```python
class Scansion:
    VOWELS = "aeiouyAEIOUYāēīōūĀĒĪŌŪ"
    DIPHTHONGS = ["ae", "au", "ei", "eu", "oe", "ai", "oi", "ou"]

    def __init__(self):
        self.scan = []
        self.reasons = []
        self.workings = 0
        self.elided = []
        self.magic = []

    def process_line(self, line):
        cleaned_line = self.clean_line(line)
        for i, char in enumerate(cleaned_line):
            if char in self.VOWELS:
                self.handle_vowel(cleaned_line, i)

    def clean_line(self, line):
        return ''.join(filter(lambda x: x in self.VOWELS or x == ' ', line))

    def handle_vowel(self, line, index):
        # Logic for handling the vowel at the given index
        pass

# Usage
if __name__ == "__main__":
    scansion = Scansion()
    line = input("line? ")
    scansion.process_line(line)
```

### Conclusion
By applying these suggestions, you can improve the structure, readability, and maintainability of your code. This will make it easier to extend and debug in the future.
>>> 
"""


"""The provided Python code is an attempt to scan Latin poetry in Dactylic Hexameter, which is a specific metrical pattern used in classical Latin poetry. The code includes various functions to analyze the syllables of a given line of Latin text, determine whether they are long or short, and handle specific cases such as elisions and diphthongs.

### Key Features of the Code:
1. **Global Variables**: The code uses several global variables to keep track of the scanning process, including `scan`, `workings`, `magic`, `elided`, and `reasons`.

2. **Functions**:
   - `procedge`: Handles specific edge cases in the scanning process.
   - `logic`: Contains the main logic for determining the length of syllables based on the context of the surrounding letters.
   - `logictf` and `logicend`: Handle the special cases for the beginning and end of the line.
   - `sigma`: Converts the scanned results into a more readable format, replacing vowels with their long or short counterparts.
   - `takeit`: The main function that processes the input line, cleans it, and applies the scanning logic.

3. **Handling of Vowels**: The code includes logic to determine whether vowels are long or short based on their context, including handling diphthongs and elisions.

4. **Output**: The final output includes the original line, the scanned line with long and short vowels marked, and a summary of the feet (Dactyls, Spondees, Trochees).

### Potential Issues:
1. **Complexity**: The code is quite complex and may be difficult to maintain or debug. It could benefit from refactoring, such as breaking down large functions into smaller, more manageable ones.

2. **Edge Cases**: While the code attempts to handle various edge cases, there may still be scenarios in Latin poetry that are not accounted for, especially with less common words or forms.

3. **Performance**: The use of global variables can lead to unexpected behavior if the functions are called multiple times in succession without resetting the state.

4. **Testing**: The code lacks a structured testing framework. It would be beneficial to implement unit tests to ensure that each function behaves as expected.

5. **Documentation**: While there are some comments, the code would benefit from more comprehensive documentation explaining the purpose of each function and the overall logic.

### Conclusion:
The code has the potential to properly scan Latin poetry in Dactylic Hexameter, but it may require further refinement and testing to ensure accuracy and reliability. If you are looking to improve or validate this code, consider focusing on edge cases, simplifying the logic, and implementing a testing framework.
"""