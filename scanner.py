scan = []
furthercheck = False
workings = 0
magic = []
elided = []
reasons = []

def procedge(instructions):
    global reasons
    global scan
    for i in range(len(instructions)):
        if instructions[i] == "-":
            reasons = reasons[:len(reasons)-1]
            scan = scan[:len(scan)-1]
        if instructions[i] == "L":
            reasons += ["edge"]
            scan += ["L"]
        if instructions[i] == "S":
            reasons += ["edge"]
            scan += ["S"]
        if instructions[i] == ".":
            return("no dipthong")
    return("return")
def logic(cont, ind): #general logic
    global scan
    global furthercheck
    global workings
    global elided
    global reasons
    global magic
    global sussyI
    vowels = "aeiouyAEIOUYāēīōūĀĒĪŌŪŷȳ"
    vowel = cont[2]
    print(vowel)
    
    #these are edge cases that cannot be caught in the algorithm but
    #are nonetheless consistent enough in literature to make a special case
    #for example, in the word sanguine, the u is not a vowel for various reasons that can't be detected with just letter placement
    edge = {"nguine":"", "deum":"-S.", "deus":"-S."} 
    workings += 1
    if vowel in "āēīōūĀĒĪŌŪȳ":
        scan += ["L"]
        print("long vowel")
        reasons += ["long vowel"]
        if furthercheck == True: # i must be the vowel in this case, and it must be non-consonantal
            magic = magic[:-1]
            furthercheck = False
            print("further check recorded")
        return()
    print(cont)
    print(edge)
    bleh = ""
    nd=False#assuming nd = no dipthong
    for key in edge:
        bleh = ""
        if cont in key:
            print("LERFAEHFUAEHDOUASDHB:OAUDHA:OSDH:AOSFH:AOSFI:OAD")
            bleh = procedge(edge[key])
            if bleh == "return":
                return()
            elif bleh == "no dipthong":
                nd = True
            
    prechecks = "none rn"
    #dipthong precheck
    if (cont[1] in vowels) or (cont[1] == " " and cont[0] in vowels) or (cont[1] == " " and vowel == "i"):
        prechecks = "erm"
    if ( #elisions
        len(cont) == 6 and #make sure it doesnt break from cont length issues #note that the start of the next word, if a Y, is not a vowel!!
        ((cont[3:5] == "m " and cont[5] in vowels) or #m elision - ignores if prior
        (cont[3] == " " and cont[4] in vowels) or #space elision - ignores if prior
        (cont[3] == " " and cont[4] == "h" and cont[5] in vowels)) #h elision - ignores if prior
        ):
        
        #need to do additional check for consonantal i
        if cont[4] == "i":
            if (cont[3] == " " and cont[5] in vowels): # i starts word and followed by vowel, is consonantal
                pass #don't elide
        else:
            print("elided")
            workings -= 1
            elided += [ind]
            return()
    elif cont[3:5] == "m " and cont[5] == "i": #m elision w/ i as 2nd vowel - look deeper
        furthercheck = True
        print("elided with 2nd I, checking deeper")
        return()
    
    #    L L s
    #    L s L
    #    s L L
    if cont[3] == " ":
        let1 = cont[4]
        let2 = cont[5]
    elif cont[4] == " ":
        let1 = cont[3]
        let2 = cont[5]
    else:
        let1 = cont[3]
        let2 = cont[4]
    if ( #double consonants
        ((let1 not in "aeiouyāēīōūȳ" and let2 not in "aeiouyāēīōūȳ") or
        (let1 in "xz" or let2 in "xz") ) and
        (not (let1 in "bpcgdt" and let2 in "rl")) and
        ((let1 + let2) != "th")
        ):
        """
        if ( #double consonants
            ((cont[3] not in "aeiou " and cont[4] not in "aeiou ") or  #Consonant Consonant
            (cont[3] not in "aeiou " and cont[4] == " " and cont[5] not in "aeiou ") or #Consonant space Consonant
            (cont[3] == " " and cont[4] not in "aeiou " and cont[5] not in "aeiou ") or #space Consonant Consonant
            (cont[3] in ["x", "z"])) and #x and z count as double consonants by themselves, interestingly
            ((not (cont[3] in "bpcgdt" and cont[4] in "rl"))) #Bad Pupils Chew Gum During Tests @ R L
        ):
        """
        print("Prechecked")
        if prechecks == "erm":
            prechecks = "double consonant"
        else:
            scan += ["L"]
            print(scan)
            reasons += ["Double consonant"]
            return()
    
    if vowel == "a":
        if cont[2:4] in ["ae", "au", "ai"] and not nd:#dipthongs - long
            scan += ["L"]
            reasons += ["Diphthong"]
        elif prechecks == "double consonant":
            scan += ["L"]
            reasons += ["Double consonant"]
        else:
            scan += ["?"]
            reasons += ["Filled in"]
    elif vowel == "e":
        if cont[1:3] in ["ae", "oe"] and not nd: #dipthongs - ignore
            print("dipthong ending")
            workings -= 1
            return()
        elif cont[2:4] in ["ei", "eu"] and not nd:#dipthongs - long
            scan += ["L"]
            reasons += ["Diphthong"]
            return()
        elif prechecks == "double consonant":
            scan += ["L"]
            reasons += ["Double consonant"]
        else:
            scan += ["?"]
            reasons += ["Filled in"]
    elif vowel == "i":
        if cont[1:3] in ["ei", "oi"] and not nd:#dipthongs - ignore 
            print("dipthong ending")
            workings -= 1
            return()
        elif (  #consonantal I
                (cont[1] == " " and cont[3] in vowels) or #starts word and followed by vowel
                (cont[1] in vowels and cont[3] in vowels) #between 2 other vowels (intervocalic)
            ):
            
            print("consonantal I")
            if furthercheck == True:
                scan += ["L"]
                reasons += ["Double consonant (with consonantal I)"]
                furthercheck = False
                print("further checks recorded")
            workings -= 1
            return()
        elif prechecks == "double consonant":
            scan += ["L"]
            reasons += ["Double consonant"]
        else:
            scan += ["?"]
            reasons += ["Filled in"]
        if furthercheck == True:
            print("further check removed")
            furthercheck = False
            elided += [ind-2]
            magic = magic[:-1]
    elif vowel == "o":
        if (cont[2:4] in ["oe", "ou"] or (cont[2:4] == "oi" and cont[4] not in "aeiou")) and not nd:#dipthongs - long
            scan += ["L"]
            reasons += ["Dipthong"]
        elif prechecks == "double consonant":
            scan += ["L"]
            reasons += ["Double consonant"]
        else:
            scan += ["?"]
            reasons += ["Filled in"]
    elif vowel == "u":
        if cont[1:3] in ["qu", "ou", "au", "eu"] and not nd:#dipthongs - ignore
            print("dipthong ending")
            workings -= 1
            return()
        elif prechecks == "double consonant":
            scan += ["L"]
            reasons += ["Double consonant"]
        else:
            scan += ["?"]
            reasons += ["Filled in"]
    elif vowel == "y":
        if cont[1] == " ":
            print("not a vowel (start of sentance)")
            workings -= 1
            return() #not a vowel if at start of sentence
        elif prechecks == "double consonant":
            scan += ["L"]
            reasons += ["Double consonant"]
        else:
            scan += ["?"]
            reasons += ["Filled in"]
    print("added")
    print(scan)
def logictf(cont, ind): #logic for the start
    global scan
    global workings
    global reasons
    vowel = cont[ind]
    workings += 1
    if ind < 2:
        if ( #elisions
            ((cont[ind+1:ind+3] == "m " and cont[ind+3] in "aeiou") or #m elision - ignores if prior
            (cont[ind+1] == " " and cont[ind+2] in "aeiou") or #space elision - ignores if prior
            (cont[ind+1] == " " and cont[ind+2] == "h" and cont[ind+3] in "aeiou")) #h elision - ignores if prior
            ):
            print("elided")
            workings -= 1
            return()
        if ind == 0:
            if cont[ind] == "i" and cont[ind+1] in "aeiou":
                workings -= 1
                return() #consonantal I
            else:
                scan += ["L"] #otherwise must be first vowel
                reasons += ["First vowel"]
        elif ind == 1:
            if vowel == "a":
                if cont[0] in "aeiou":
                    scan += ["?"]
                    reasons += ["Filled in"]
                else:
                    scan += ["L"] #can never be end of dipthong / elide, so auto long
                    reasons += ["First vowel"]
            elif vowel == "e":
                if cont[0:2] == "ae":
                    return()
                elif cont[0] in "aeiou":
                    scan += ["?"]
                    reasons += ["Filled in"]
                else:
                    scan += ["L"]
                    reasons += ["First vowel"]
            elif vowel == "i":
                if cont[0:2] in ["ei", "oi"]:
                    workings -= 1
                    return()
                elif cont[0] in "aeiou":
                    scan += ["?"]
                    reasons += ["Filled in"]
                else:
                    scan += ["L"]
                    reasons += ["First vowel"]
            elif vowel == "o":
                if cont[0] in "aeiou":
                    scan += ["?"]
                    reasons += ["Filled in"]
                else:
                    scan += ["L"]
                    reasons += ["First vowel"]
            elif vowel == "u":
                if cont[0:2] in ["qu", "ou", "au", "eu"]:
                    workings -= 1
                    return()
                elif cont[0] in "aeiou":
                    scan += ["?"]
                    reasons += ["Filled in"]
                else:
                    scan += ["L"]
                    reasons += ["First vowel"]
    print(scan)
    
def logicend(cont, ind):
    global scan
    global workings
    global reasons
    print(ind)
    ind = 4+ind
    vowel = cont[ind]
    print(vowel)
    print(ind)
    workings += 1
    
    if vowel == "a":
        scan += ["X"]
        reasons += ["Last vowel"]
    elif vowel == "e":
        if cont[ind-1:ind+1] == "ae":
            workings -= 1
            return()
        else:
            scan += ["X"]
            reasons += ["Last vowel"]
    elif vowel == "i":
        if cont[ind-1:ind+1] in ["ei", "oi"]:
            workings -= 1
            return()
        else:
            scan += ["X"]
            reasons += ["Last vowel"]
    elif vowel == "o":
        scan += ["X"]
        reasons += ["Last vowel"]
    elif vowel == "u":
        if cont[ind-1:ind+1] in ["qu", "ou"]:
            workings -= 1
            return()
        else:
            scan += ["X"]
            reasons += ["Last vowel"]
    else:
        scan += ["X"]
        reasons += ["Last vowel"]

    print(scan)
    

#this function takes a line of poetry and a scan (the scan does not need to be complete)
#it adds long marks and short marks to the vowels in the line of poetry according to the scansion provided
def sigma(scan, line): 
    #āēīōū
    #ă, ĕ, ĭ, ŏ, ŭ
    #Ā, Ē, Ī, Ō, Ū
    #Ă, Ĕ, Ĭ, Ŏ, Ŭ
    scannedline = list(line)
    used = 0
    print(magic)
    for i in range(len(scannedline)):
        print(i)
        if i in magic:
            print(scan[used:])
            print("".join(scannedline[i:]))
            """match scannedline[i]:
                case "a":
                    if scan[used] == "L":
                        scannedline[i] = "ā"
                    elif scan[used] == "S":
                        scannedline[i] = "ă"
                    else:
                        scannedline[i] = "a"
                case "e":
                    if scan[used] == "L":
                        scannedline[i] = "ē"
                    elif scan[used] == "S":
                        scannedline[i] = "ĕ"
                    else:
                        scannedline[i] = "e"    
                case "i":
                    if scan[used] == "L":
                        scannedline[i] = "ī"
                    elif scan[used] == "S":
                        scannedline[i] = "ĭ"
                    else:
                        scannedline[i] = "i"
                case "o":
                    if scan[used] == "L":
                        scannedline[i] = "ō"
                    elif scan[used] == "S":
                        scannedline[i] = "ŏ"
                    else:
                        scannedline[i] = "o"
                case "u":
                    if scan[used] == "L":
                        scannedline[i] = "ū"
                    elif scan[used] == "S":
                        scannedline[i] = "ŭ"
                    else:
                        scannedline[i] = "u"
                case "y":
                    if scan[used] == "L":
                        scannedline[i] = "ȳ"
                    elif scan[used] == "S":
                        scannedline[i] = "ŷ"
                    else:
                        scannedline[i] = "y" """
            if scannedline[i] == "a" or scannedline[i] == "A":
                if scan[used] in ["L", "X"]:
                    scannedline[i] = "ā"
                elif scan[used] == "S":
                    scannedline[i] = "ă"
                else:
                    scannedline[i] = "a"
            elif scannedline[i] == "e" or scannedline[i] == "E":
                if scan[used] in ["L","X"]:
                    scannedline[i] = "ē"
                elif scan[used] == "S":
                    scannedline[i] = "ĕ"
                else:
                    scannedline[i] = "e"
            elif scannedline[i] == "i" or scannedline[i] == "I":
                if scan[used] in ["L", "X"]:
                    scannedline[i] = "ī"
                elif scan[used] == "S":
                    scannedline[i] = "ĭ"
                else:
                    scannedline[i] = "i"
            elif scannedline[i] == "o" or scannedline[i] == "O":
                if scan[used] in ["L", "X"]:
                    scannedline[i] = "ō"
                elif scan[used] == "S":
                    scannedline[i] = "ŏ"
                else:
                    scannedline[i] = "o"
            elif scannedline[i] == "u" or scannedline[i] == "U":
                if scan[used] in ["L", "X"]:
                    scannedline[i] = "ū"
                elif scan[used] == "S":
                    scannedline[i] = "ŭ"
                else:
                    scannedline[i] = "u"
            elif scannedline[i] == "y":
                if scan[used] in ["L", "X"]:
                    scannedline[i] = "ȳ"
                elif scan[used] == "S":
                    scannedline[i] = "ŷ"
                else:
                    scannedline[i] = "y"
            used += 1
    print(len(scan))
    print(used)
    scannedline = "".join(scannedline)
    print(scannedline)
    return(scannedline)
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main code~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def takeit(line2):
    #take in line of latin
    global scan
    global workings
    global magic
    global elided
    global reasons
    
    scan = []
    workings = 0
    magic = []
    elided = []
    reasons = []
    problems = [] #potential problems with the inputted line
    
    line=""
    for letter in line2: #remove non letters
        if letter.lower() in "abcdefghijklmnopqrstuvwxyz āēīōūŷ":
            line += letter
    for i in range(len(line)-1):
        if line[i] == " " and line[i+1] == " ":
            print(line)
            line=line[:i] + line[i+1:]
            print(line)
            
    #do sanity checks on the input
    if len(line.split())<4:
        problems += ["too short to be a full line of poetry"]
    elif len(line.split())>18:
        problems += ["too long to be a single line of poetry"]

    #go through every vowel and do specific logic for each
    for i in range(len(line)):
        if line[i].lower() in "aeiouāēīōūyŷ":
            print(i)
            working = workings
            if i > 1 and i <= len(line)-3: #middle
                context = line[i-2:i+4].lower() #len 6
                print(context)
                print(line[i])
                logic(context, i)
                print(len(line))
            elif i < 2: #start
                context = line[:6].lower()
                print(context)
                logictf(context, i)
            elif i > len(line)-3: #end
                print(i)
                print(len(line))
                print(line[i])
                context = line[len(line)-4:].lower()
                print(context)
                print(i-len(line))
                logicend(context,i-len(line))
            else:
                logic(context, i)
            if working != workings:
                magic += [i]
            print(reasons)
            print(magic)
            print(len(reasons), len(magic), "smthn man")
                
    print(scan)
    if scan[len(scan)-4] == "L" or scan[len(scan)-3] == "L":
        problems += ["!! Something wrong with 5th foot, syllable previously determined long forced to be short !!"]
    scan[len(scan)-5:len(scan)] = ["L","S", "S", "L", "X"] #auto scan last 2 feet
    print(scan)
    print(len(scan))
    dactyls = len(scan) - 12 - 1
    step1 = sigma(scan, line)
    
    if len(scan) > 18:
        problems += ["too many syllables to be a line of poetry"]
    elif len(scan) < 12:
        problems += ["too few syllables to be a line of poetry"]

    print("filling in")
    feet = []
    feet = ["".join(scan[len(scan)-2:len(scan)])] + feet
    feet = ["".join(scan[len(scan)-5:len(scan)-2])] + feet
    print(feet)
    feetnum = len(scan)-5
    print("dactyls:")
    print(dactyls)
    
    #fill in the blanks
    feetOutputs = createfeet(feetnum, scan, feet, dactyls)
    possibleScans = []
    possibleFeet = []
    #unpack output of function
    for i in range(len(feetOutputs)):
        print("POSSIBILITIES")
        print(feetOutputs)
        possibleScans.append(feetOutputs[i][0])
        possibleFeet.append(feetOutputs[i][1])
    scan = possibleScans[0]
    feet = possibleFeet[0]
    print("SCAN")
    print(scan)
    print("FEET")
    print(feet)
    
    print("FEEEEEEEEEEET")
    print(feet)
    
    
    if len(feet) > 6:
        problems += ["too many feet to be a line of poetry"]
    elif len(feet) < 6:
        problems += ["too few feet to be a line of poetry"]
        
    verbalFeet = verbalizeFeet(feet)
    
    step2 = sigma(scan.copy(), line[:])
    
        
    elidOut = ""
    for j in elided:
        startoffirstword = None
        for i in range(len(line)):
            if line[i] == " " and len([x for x in line[i:j+1] if x == " "]) == 1:
                startoffirstword = i+1
            elif len([x for x in line[j:i+1] if x == " "]) == 2:
                elidOut += "Elision between: " + str(line[startoffirstword:i]) + "\n"
                place = line[j:i+1].index(" ")+j
                step2 = step2[:place] + "_" + step2[place+1:] #inserting elision mark

                break
    elidOut = elidOut[:-1]
    
    result = ""
    result += "Original line: \n"
    result += line2
    result += "\n\nStep 1: "
    result += step1
    result += "\n\nStep 2: "
    result += step2
    result += "\n\nFinal Scansion:\n"
    for foot in feet:
        result += foot+", "
    result = result[:-2]
    result += "\n" + verbalFeet
    result += "\n" + stocking(step2)
    
    if len(possibleScans)>1:
        result += "\n\nOther option(s):\n"
        for i in range(len(possibleScans)):
            if i == 0:
                pass
            else:
                result += sigma(possibleScans[i], line) +"\n"
                for foot in possibleFeet[i]:
                    result += foot+", "
                result += "\n" + verbalizeFeet(possibleFeet[i])
                result += "\n" + stocking(sigma(possibleScans[i].copy(), line[:]))
                result += "\n\n"
    
    result += "\n\n"+elidOut
    
    if problems:
        result += "\nProblems with input:"
        for problem in problems:
            result += "\n" +problem
            
    
    print(reasons)
    print(len(reasons))
    print(len(scan))
          
    #reset variables
    scan = []
    furthercheck = False
    workings = 0
    magic = []
    problems = []
    print("RECURSION: \n", possibleScans, possibleFeet)
    return(result)

def stocking(scannedline): # adding || between feet on output (like putting on socks)
    longs = "āēīōūĀĒĪŌŪ"
    shorts = "ăĕĭŏŭŷ"
    vowelsinfoot = 0
    i=0
    while i != len(scannedline): #while loop to accomodate the changing length of the string
        if scannedline[i] in longs:
            vowelsinfoot += 2
        elif scannedline[i] in shorts:
            vowelsinfoot += 1
        if vowelsinfoot == 4 and i < len(scannedline)-2:
            scannedline = scannedline[:i+1] + "||" + scannedline[i+1:]
            vowelsinfoot = 0
        i+=1
    return scannedline

def createfeet(lastFootIndex, option0, output0, numDac, start=0):
    options = [option0]
    outputs = [output0]
    length = len(options[0]) - 6
    if start:
        length = start
    for i in range(length, 0, -1):
        changenum = lastFootIndex #FEETNUM IS THE INDEX OF THE LAST FOOT
        if options[0][i] == "?":
            if options[0][i-1] == "L" and options[0][i+1] == "L": #squished between two longs, must be long
                options[0][i] = "L"
                outputs[0] = ["".join(options[0][i-1:i+1])] + outputs[0]
                lastFootIndex = i-1
            elif options[0][i+1] == "L" and lastFootIndex != i+1: #if next vowel is long and is not the start of a foot, current vowel must be long, start of spondee
                options[0][i] = "L"
                outputs[0] = ["".join(options[0][i-1:i+1])] + outputs[0]
                lastFootIndex = i
            elif options[0][i-1] == "?" and numDac > 0: #when in doubt, dactyl
                if options[0][i-2] == "?" and options[0][i-3] == "?" and (i > numDac*3): #four question marks in a row, and the rest of the scan isn't guaranteed to be dactyls
                    #make these two a spondee and go recursive mode on this shit
                    bleh = len(options) #need to keep this consistent
                    options.append(options[0].copy()) #len(options) in order to create a new potential outcome
                    outputs.append(outputs[0].copy()) #copy over current progress
                    
                    options[bleh][i] = "L" #make spondee
                    options[bleh][i-1] = "L"
                    outputs[bleh] = ["".join(options[bleh][i-1:i+1])] + outputs[bleh]
                    lastFootIndex = i-1
                    
                    #send into recursion 
                    newStuff = createfeet(lastFootIndex, options[bleh].copy(), outputs[bleh].copy(), numDac, start=i-1) 
                    lastFootIndex = changenum #undo index shit
                    
                    options.pop()
                    outputs.pop()
                    
                    for j in range(len(newStuff)):
                        #add new outcomes
                        print("NEWSTUFF", j, ":\n", newStuff)
                        options.append(newStuff[j][0])
                        outputs.append(newStuff[j][1])
                    
                #regardless of the recursion stuff, continue "when in doubt, dactyl"
                options[0][i] = "S"
                options[0][i-1] = "S"
                options[0][i-2] = "L" #create the dactyl
                outputs[0] = ["".join(options[0][i-2:i+1])] + outputs[0] #add to feet
                lastFootIndex = i-2 #set start of latest foot to the start of the dactyl
                numDac -= 1 #reduce the amount of dactyls remaining
        
            elif numDac == 0: #lowk this should be the first condition
                options[0][i] = "L"
        if options[0][i] == "L" and changenum == lastFootIndex and i != 0:
            if i != lastFootIndex:
                options[0][i-1] = "L"
                outputs[0] = ["".join(options[0][i-1:i+1])] + outputs[0]
                lastFootIndex = i-1
        print(options[0])
        print(outputs[0])
        
    GETOUT = [] #reference to adrian meme, list of scan, feet pairs
    for i in range(len(options)):
        print("OPTIONS")
        print(options, outputs)
        GETOUT.append([options[i], outputs[i]])
    print(len(GETOUT))
    return(GETOUT)

def verbalizeFeet(listFeet):
    feet3 = ""
    for thing in listFeet:
        if thing == "LL":
            feet3 += "Spondee"
        elif thing == "LSS":
            feet3 += "Dactyl"
        else:
            feet3 += "Trochee"
        feet3 += ", "
    feet3 = feet3[:-2]
    return(feet3)

if __name__ == "__main__":
    print(takeit(input("line? ")))
else:
    def print(*args, **kwargs):
        pass

#dipthongs
# ae, au, ei, eu, oe, and, in early Latin, ai, oi, ou.


#also work on groups- use classes, wonderful practice
#armaque Trojanoque a sanguine clarus Acestes

#working lines
#Arma virumque canō, Trōiae qui primus ab oris
#Italiam fato profugus Laviniaque venit - lavinIA, no reasoning to not consider the last I as it should
    #if you KNOW the i is consonantal or otherwise shouldnt be considered, use a j instead of i
    #using j is only necessary if there is truly no observable logic for the i to be consonantal otherwise
    #fixed
#litora, multum ille et terris iactatus et alto
#vi superum saevae memorem Iunonis ob iram - doesnt work because of elision at memorEm Iunonis - fixed
#multa quoque et bello passus, dum conderet urbem
#inferretque deos Latio; genus unde Latinum
#Albanique patres atque altae moenia Romae.
#Musa, mihi causas memora, quo numine laeso - why should it be 
    #- Mūsă, mĭh|ī caūs|ās mĕmŏr|ā, quō| nūmĭnĕ| laēsō -instead of
    #- Mūsă, mĭh|ī caūs|ās mēm|ōră, quŏ| nūmĭnĕ| laēsō -which the bot spits out? quo is prolly ablative, but how tell the bot?
    #- Mūsă, mĭh|ī cāus|ās mēm|ōră, quŏ| nūmĭnĕ| lāeso
    #check for common ablatives?
    #accept ō as a character? - yes
    #fixed, but should we return the full line with longs and shorts on vowels?
    #Musa, mihi causas memora, quō numine laeso
#quidve dolens regina deum tot volvere casus
# wrong again ahaha
#insignem pietate virum, tot adire labores
#impulerit. tantaene animis caelestibus irae?



#problem lines - all fixed :)
#still need to figure out semivowel U in sanguine

#figure out start and end stuff, mostly start stuff, and at the end if vowel isnt in the last 3 letters
#just say at the start, "if scan is empty before you add this first vowel scansion, then make it long"

#incubuere marī totumque a sedibus imis
#ī 

#find problem lines

#ceasuras? accipiunt inimicum imbrem rimisque fatiscunt.

#ȳŷȲ
