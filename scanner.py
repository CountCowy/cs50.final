scan = []
furthercheck = False
workings = 0
magic = []
elided = []
reasons = []
def print(*args, **kwargs):
    pass

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
    vowels = "aeiouyAEIOUYāēīōūĀĒĪŌŪŷȳ"
    vowel = cont[2]
    print(vowel)
    edge = {"nguine":"", "deum":"-S.", "deus":"-S."}
    workings += 1
    if vowel in "āēīōūĀĒĪŌŪȳ":
        scan += ["L"]
        print("long vowel")
        reasons += ["long vowel"]
        if furthercheck == True: # i must be the vowel in this case, and it must but non-consonantal
            magic = magic[:-1]
            furthercheck = False
            print("further check recorded")
        return()
    print(cont)
    print(edge)
    bleh = ""
    nd=False
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
    if (cont[1] in "aeiouyāēīōūȳ") or (cont[1] == " " and cont[0] in "aeiouyāēīōūȳ") or (cont[1] == " " and vowel == "i"):
        prechecks = "erm"
    if ( #elisions
        len(cont) == 6 and #make sure it doesnt break from cont length issues #note that the start of the next word, if a Y, is not a vowel!!
        ((cont[3:5] == "m " and cont[5] in "aeouāēīōū") or #m elision - ignores if prior
        (cont[3] == " " and cont[4] in "aeiouāēīōū") or #space elision - ignores if prior
        (cont[3] == " " and cont[4] == "h" and cont[5] in "aeiouāēīōū")) #h elision - ignores if prior
        ):
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
def logictf(cont, ind): #logic for the start and finish
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
                if cont[0:2] in ["qu", "ou"]:
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
    
def sigma(scan, line):
    #āēīōū
    #ă, ĕ, ĭ, ŏ, ŭ
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
            if scannedline[i] == "a":
                if scan[used] in ["L", "X"]:
                    scannedline[i] = "ā"
                elif scan[used] == "S":
                    scannedline[i] = "ă"
                else:
                    scannedline[i] = "a"
            elif scannedline[i] == "e":
                if scan[used] in ["L","X"]:
                    scannedline[i] = "ē"
                elif scan[used] == "S":
                    scannedline[i] = "ĕ"
                else:
                    scannedline[i] = "e"
            elif scannedline[i] == "i":
                if scan[used] in ["L", "X"]:
                    scannedline[i] = "ī"
                elif scan[used] == "S":
                    scannedline[i] = "ĭ"
                else:
                    scannedline[i] = "i"
            elif scannedline[i] == "o":
                if scan[used] in ["L", "X"]:
                    scannedline[i] = "ō"
                elif scan[used] == "S":
                    scannedline[i] = "ŏ"
                else:
                    scannedline[i] = "o"
            elif scannedline[i] == "u":
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
    
    line=""
    for letter in line2: #remove non letters
        if letter.lower() in "abcdefghijklmnopqrstuvwxyz āēīōūŷ":
            line += letter
    for i in range(len(line)-1):
        if line[i] == " " and line[i+1] == " ":
            print(line)
            line=line[:i] + line[i+1:]
            print(line)

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
    scan[len(scan)-5:len(scan)] = ["L","S", "S", "L", "X"] #auto scan last 2 feet
    print(scan)
    print(len(scan))
    dactyls = len(scan) - 12 - 1
    step1 = sigma(scan, line)

    print("filling in")
    feet = []
    feet = ["".join(scan[len(scan)-2:len(scan)])] + feet
    feet = ["".join(scan[len(scan)-5:len(scan)-2])] + feet
    print(feet)
    feetnum = len(scan)-5
    print("dactyls:")
    print(dactyls)

    for i in range(len(scan) - 6, 0, -1):
        changenum = feetnum #FEETNUM IS THE INDEX OF THE LAST FOOT
        if scan[i] == "?":
            if scan[i-1] == "L" and scan[i+1] == "L": #squished between two longs, must be long
                scan[i] = "L"
                feet = ["".join(scan[i-1:i+1])] + feet
                feetnum = i-1
            elif scan[i+1] == "L" and feetnum != i+1: #if next vowel is long and is not the start of a foot, current vowel must be long, start of spondee
                scan[i] = "L"
                feet = ["".join(scan[i-1:i+1])] + feet
                feetnum = i
            elif scan[i-1] == "?" and dactyls > 0: #when in doubt, dactyl
                scan[i] = "S"
                scan[i-1] = "S"
                scan[i-2] = "L"
                feet = ["".join(scan[i-2:i+1])] + feet
                feetnum = i-2
                dactyls -= 1
            elif dactyls == 0:
                scan[i] = "L"
        if scan[i] == "L" and changenum == feetnum and i != 0:
            if i != feetnum:
                scan[i-1] = "L"
                feet = ["".join(scan[i-1:i+1])] + feet
                feetnum = i-1
        print(scan)
        print(feet)

        

    feet2 = []
    feet2 = ["".join(scan[len(scan)-2:len(scan)])] + feet2
    feet2 = ["".join(scan[len(scan)-5:len(scan)-2])] + feet2
    skip = 0
    for i in range(len(scan) -6, 0, -1):
        if skip:
            skip -= 1
            pass
        elif scan[i] == "L" and scan[i-1] == "L":
            feet2 = ["".join(scan[i-1:i+1])] + feet2
            skip = 1
        elif scan[i] == "S" and scan[i-1] == "S" and scan[i-2] == "L":
            feet2 = ["".join(scan[i-2:i+1])] + feet2
            skip = 2
        else:
            feet2 = ["".join(scan[i])] + feet2
    print()
    print(feet2)
    
    print("FEEEEEEEEEEET")
    print(feet)
    feet3 = ""
    for thing in feet:
        if thing == "LL":
            feet3 += "Spondee"
        elif thing == "LSS":
            feet3 += "Dactyl"
        else:
            feet3 += "Trochee"
        feet3 += ", "
    feet3 = feet3[:-2]
    
    step2 = sigma(scan, line)
    
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
    result += "\n" + feet3
    result += "\n" + stocking(step2)
    
    
    result += "\n\n"+elidOut
    
    print(reasons)
    print(len(reasons))
    print(len(scan))
          
    #reset variables
    scan = []
    furthercheck = False
    workings = 0
    magic = []
    return(result)

def stocking(scannedline):
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

if __name__ == "__main__":
    print(takeit(input("line? ")))

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

#ȳŷ
