## **1. Title & Overview**

**Project Name:** Constant's Scanner 
**Description:**  
A web application for scanning Latin poetry in dactylic hexameter, using a custom algorithm, OpenAI assistance, Supabase for data storage, Flask for backend logic, Bootstrap/Jinja for the frontend, and Vercel for serverless deployment

**Goals:**

- Provide automatic scansion of Latin verse.
    
- Provide an OpenAI-assisted interpretation or alternative scansion.
    
- Maintain user accounts with login + email verification.
    
- Store users’ past scans.
    
- Provide a contact form to message the site owner.
    

---
### !! Important !!
Before going into how the webapp works, it is important to have at least a surface level understanding for what scansion in Latin poetry is. A better, more in depth introduction can be found from online materials such as **Allen and Greenough**'s book on latin grammar. 
Latin poetry is written in meter which determines how the syllables are stressed.
- This is the same way that Shakespeare's plays, when spoken aloud or performed, are supposed to put emphasis on every-other syllable (duh DUH duh DUH). 
- The meter that this web app focuses on is dactylic hexameter, which splits each line into 6 feet of spondees and dactyls.
- A spondee has two long syllables, denoted by a long dash over the syllable. These longs syllable are, you guessed it, held at a longer length when pronounced, somewhat similar to how you emphasize every-other syllable in Shakespeare
- A dactyl has one long syllable followed by two short syllables. Long syllables are still denoted with a long dash, while short syllables have what looks like a "u" above each one. Long syllables are, like before, held for a longer length when pronounced, while short syllables are conversely held at a shorter length. 
- Every line of poetry in dactylic hexameter must have 6 feet in some combination of spondees and dactyls. (that's the HEX part in hexameter)
- A key feature of dactylic hexameter is that the second to last foot is (almost) always a dactyl and the very last foot is always either a spondee or a troche (which is glossed in this algorithm as a spondee). This allows the algorithm to ignore the last 5 syllables
- Here is an example of scansion from the sixth line of the Aeneid:
	- The line here is: inferretque deos Latio, genus unde Latinum
	- This line gets scanned: īnfē || rrētquĕ dĕ || ōs Lătĭ || ō gĕnŭ || s ūndĕ Lă || tīnūm
		- there is a || in between every foot
		- Spondee Dactyl Dactyl Dactyl Dactyl Spondee
- Another important piece of information is concerning the relationship between the number of syllables, the number of spondees and the number of dactyls
	- Let N be the number of syllables in a line, S be the number of spondees and D be the number of dactyls. 
	- From the rules of dactylic hexameter, we know D+S = 6, aka S=6-D
	- We also know that a spondee has 2 syllables (2 long syllables) and a dactyl has 3 syllables (1 long and 2 short), so N = 2S + 3D
	- Substituting S = 6-D, we have N = 2(6-D) + 3D or N = 12+D
	- This can be rewritten D=N-12, so the number of dactyls in a given line of dactylic hexameter is 12 less than the number of syllables
	- This is crucial information for the algorithm to work, since there is not much information given to the algorithm in the first place
That is a very rough introduction to scansion. As stated before, there are other, better materials online, such as **Allen and Greenough**'s book on latin grammar. 
## **2. System Architecture**

### **2.1 High-Level Diagram**

Example bullet version:

- **Client Browser**  
    → Sends requests, interacts with forms, uses Bootstrap UI.
    
- **Flask Server (Backend)**
    
    - Handles routes
        
    - Applies authentication (login_required)
        
    - Requests the scansion algorithm
        
    - Sends OpenAI API requests
        
    - Database queries to Supabase
        
- **Supabase Backend**
    
    - Authentication
        
    - RLS-protected tables (messages, scans, users)
        
    - Storage of scan history
        
- **OpenAI API**
    
    - Used for optional scansion help
        
- **Vercel Hosting**
    
    - Serves Flask app via serverless deployment
        

---

## **3. Data Model**

### **3.1 Tables**

#### **users (auth handled by Supabase)**

- id (uuid)
    
- username (text)
    
- created_at (timestampz)
    

#### **messages**

- id (uuid)
    
- user_id (uuid, FK → users.id)
    
- email (text)
    
- username (text)
    
- subject (text)
    
- message (text)
    
- created_at (timestampz)
    

#### **scans**

- id (int4)
    
- user_id (uuid)
    
- input_line (text) 
    
- algorithm_scan (text)
    
- gpt_scan (text)
    
- timestamp (timestampz)
    

### **3.2 RLS Policies**

Explain the purpose:

- Users may only insert messages where `auth.uid() = user_id`
    
- Users may only read their own scan history, where `auth.uid() = user_id`
    
- Users may only access their own user information where `auth.uid() = user_id`
    
---

## **4. Core Features**

Explain each feature, how it works, and what technologies it touches.

### **4.1 Scansion Algorithm** (scanner.py)

- This file is the most significant aspect to my project, and can be broken down into the following steps
    
### 1. **Functions for Scansion Logic**
The algorithm is structured around several key functions that handle different aspects of the scanning process:

- **`logic(cont, ind)`**: This is the main function that determines the scansion of a syllable based on its context. It takes as input the two characters prior to the target vowel and three letters after the target vowel (for a total of 6 characters in the string 'cont') , and uses that to determine elision, length, and other  curcial information relevant for the scan. 

- **`logictf(cont, ind)` and `logicend(cont, ind)`**: These functions handle the special cases for the beginning and end of the line, respectively, ensuring that the first and last vowels are treated correctly according to Latin metrical rules.

### 2. **Contextual Analysis**
In logic(cont, ind), the program analyzes the context of each vowel in the line:
- First it checks whether the target vowel is elided, in which case the vowel is then on ignored and the position of the elision is marked for later use
- Next, it checks if the current vowel is long by position, as in, if the vowel is prior to two consonants, in which case the vowel can be marked as long
- Then it checks if the vowel is part of a diphthong (combination of two vowels), whether at the start or the end
	- If the vowel is the start of a diphthong, it is considered long
	- If the vowel is the second vowel of the diphthong, it is ignored for the rest of the algorithm
	- This section also checks for other cases, such as consonantal i (think of how "iulius caesar" in Latin is pronounced "Julis Caesar") or the combination of Q and U (which function as a single consonant in Latin)
- Anything that is not caught by the checks above is marked with a question mark, and is filled in by Step 2 of the algorithm
- This is all based on the 6 characters handed into the function. The entire line given by the user is processed in 6 character increments like this, except for the start and end which are handled by the similar, but slightly specialized functions logictf and logicend

### 3. **Finalizing the Scansion**
After processing the entire line (which is considered Step 1 in the final output), the program fills in any undetermined syllables based on the established rules of Latin meter. 
- This is considered Step 2 in the final output
- Essential to this section is the fact that the number of dactyls in a line is 12 less than the number of syllables, as explained prior
- The first step is to automatically mark the final 5 syllables as a dactyl + spondee, according to the conventions of dactylic hexameters
- In the createfeet function, the parts of the scansion that were not determined in step 1 are filled in
	- Somewhat of note, this function goes through the line of poetry in reverse (starting from the back, ending at the front), as I found that was the easiest way to figure out the logic
	- This uses various bits of logic built from the rules of dactylic hexameter, like, if an undetermined syllable is stuck between two long syllables, it must be long (either the start or end of a spondee)
	- Those bits of logic are not enough to fully finish every scan, so if the function encounters a significant patch of undetermined syllables, it assumes (within reason) that it is a dactyl. This method works more often then not, surprisingly.
		- just in case there is a situation where the line has enough undetermined syllables for this approach to be ambiguous (a situation where a scan can go either Dactyl spondee or Spondee dactyl), I made the function slightly recursive to catch all possible outcomes
- Once all of this is done, the final scansion is determined and all that is left is collecting all the information needed for the final output
### 4. **Output Generation**
The program generates a final output that includes:
- The original line of poetry.
- The scanned line with long and short syllables marked.
- A verbal description of the feet (dactyls, spondees, etc.) present in the line.
- The scanned line, but with all the feet separated by ||
- Any of the other possible scansions, in the case of an ambiguous situation as mentioned before
- A sentence describing the location of all elisions, if any
- Any notes on potential errors with the input or scansion process that were detected, if any

### **4.2 OpenAI-Assisted Scansion**

- ChatGPT 4-o mini is queried through the OpenAI api to provide assistive information for the user, along side the algorithmically generated output. Unfortunately ChatGPT is utterly horrendous when it comes to any task concerning scansion, perhaps due to the general lack of popularity for the topic, the lack of materials for it to train from etc. so the output is not particularly useful. It is still kept as a feature, however.
    
- Because ChatGPT is so unfamiliar with scansion, it takes a very long time to respond to prompts related to scansion, which increases the wait time after a user inputs a line of poetry
    

### **4.3 Authentication + Email Verification**

- The project uses Supabase Authentication for sign up and log in functionality. This includes sending an email with a confirmation link upon registration
    
- The Session token is the user id (uuid) found from Supabase and is stored in the browser's cookies.
    

### **4.4 Dashboard / Scan History**

- Scans are stored in a Supabase table, keeping the original line, the algorithm output, the OpenAI output, the user id inputted it, the id of the individual scan, and the time of the scan
    
- Scans are retrieved when requested on "/history" and displayed in a similar format to the original scan

### **4.5 Contact Form**

- The contact page holds simple information about myself, as well as a field for the user to send me a message which is then stored in a Supabase table
    

---

## **5. User Workflow**

Describe as a sequence of steps:

### **5.1 New User**

1. Visit homepage
    
2. Click "Sign Up"
    
3. Complete email verification
    
4. Log in
    
5. Enter Latin verse to scan
    
6. View scansion + OpenAI help
    
7. Review past scans
    
8. Send optional message to owner
    

---

## **6. API Endpoints (Flask Routes)**

### **GET /** (index)

- Renders index.html
    
- Contains main scansion interface for user to input a line of poetry
    
### **POST /** (index)

- Takes the input of a line of poetry, runs scansion algorithm and queries OpenAI, saves results in the database and redirects to the display page "/scan"
    
### **POST /scan**

- Shows the results of a scan
    
### **/login**, **/logout**, **/register**

- Handled by Supabase Auth logic in Flask
    

### **POST /contact**

- Inserts message into Supabase
    

### **/history**

- Retrieves scan logs for current user
    

---

## **7. Security Considerations**

- HTTPS enforced by Vercel
    
- RLS policies block unauthorized DB access
    
- All inserts validated server-side
    
- CSRF prevention (Flask forms or manual token)
    

---

## **8. Deployment**

- Vercel builds the Flask project serverlessly from github
    
- Environment variables stored in Vercel dashboard
    
