import variables as v


def sortMatches(matchType): #sorts our qualification matches

    matchList = v.matchList
    qmDataList = v.qmDataList
    for x in range(len(v.matches)):
        match = v.matches[x]
        type = match['comp_level']
        if type == matchType: #checks if the type is qual-match
            mn = int(match['match_number'])
            if((type == "sf") or (type == "f")):
                nonQualNum = match['key']
            if(type == "qm"):
                nonQualNum = None
            matchList.append(mn) #adds th match num list
            qmDataList.append(v.tba.match(nonQualNum, 2024, v.eventKey, matchType, int(mn)))


    print('Found all QM matches, sorting now!')

    if(matchType == "qm"):
        tempTuple = (sorted(zip(matchList, qmDataList)))
        matchList, qmDataList = list(zip(*tempTuple))
        #matchList, qmDataList = zip(*sorted(zip(matchList, qmDataList)))

    v.matchList =  list(matchList)
    v.qmDataList = list(qmDataList)

    print('Sorted!')

