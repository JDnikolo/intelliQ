from flask import request, Blueprint, jsonify
from mysqlconfig import myconnector
from authentication import authUser
from csvResponse import generateCSVresponse

getallanswers_blueprint = Blueprint("getallanswers", __name__)

@getallanswers_blueprint.route('/getallanswers/<questionnaireID>', methods = ['POST', 'GET'])
def getallanswers(questionnaireID):
    if request.method == 'GET':
        if authUser():
            args = request.args
            if (len(args) == 0):
                format = "json"
            elif (len(args) > 1):
                return jsonify({"type": "/errors/operation-error",
                            "title": "Invalid query parameters.",
                            "status": "400",
                            "detail": "Only format is acceptable query parameter.",
                            "instance": "/Users/getsessionanswers"}), 400
            elif (len(args) == 1):
                temp = args.to_dict()
                temp = temp.keys()
                temp = list(temp)
                temp = temp[0]
                if (temp != "format"):
                    return jsonify({"type": "/errors/operation-error",
                            "title": "Invalid query parameters.",
                            "status": "400",
                            "detail": "Only format is acceptable query parameter.",
                            "instance": "/Users/getsessionanswers"}), 400
                elif (args.get("format") == "json"):
                    format = "json"
                elif (args.get("format") == "csv"):
                    format = "csv"
                else:
                    return jsonify({"type": "/errors/operation-error",
                            "title": "Invalid format type.",
                            "status": "400",
                            "detail": "Only json and csv are acceptable formats.",
                            "instance": "/Users/getsessionanswers"}), 400
            sqlcursor = myconnector.cursor()
            sqlcursor.execute(''' SELECT questionID, sessionID,
            IF (STRCMP(`optionTXT`,"<open string>") != 0,
            ans_optionID, answertxt)
            FROM Answer INNER JOIN Qoption
            WHERE (optionID = ans_optionID AND qnrID = %s)
            ORDER BY questionID''',(str(questionnaireID),))
            result = sqlcursor.fetchall()
            sqlcursor.execute("SELECT DISTINCT sessionID FROM Answer WHERE (qnrID = %s)",
            (str(questionnaireID),))
            sessions = sqlcursor.fetchall()
            sqlcursor.execute("SELECT DISTINCT questionID FROM Question WHERE (qnrID = %s)",
            (str(questionnaireID),))
            questions = sqlcursor.fetchall()
            if len(result) == 0:
                return jsonify({"type": "/errors/operation-error",
                            "title": "No answers found.",
                            "status": "402",
                            "detail": "No answers were found.",
                            "instance": "/Users/getallanswers"}), 402
            sqlcursor.close()
            # Increase result to its final size (it will grow up anyway, why not now?)
            temp_size = len(result)
            while (temp_size < len(questions)*len(sessions)):
                result.append(("a","a","a"))
                temp_size = len(result)
            # Change result so that it has all questions and no answers, even with NO ANSWER
            p = 0 # pointer
            i = 0
            j = 0
            for i in range(len(questions)):
                for j in range(len(sessions)):
                    print(p)
                    if(p < len(result) and (not result[p][0] == questions[i][0] or not result[p][1] == sessions[j][0])):
                        # Question Session does not exist, add it with NO ANSWER
                        result.insert(p, (questions[i][0], sessions[j][0], "NO ANSWER"))
                    p = p + 1
                    
            # The next commented section is obsolete
            # If p <= len(sessions)*len(questions), some NO ANSWER must be appended
            '''if (p <= len(sessions)*len(questions)):
                for ii in range(i, len(questions)):
                    for jj in range(j, len(sessions)):
                        result.append((questions[ii][0], sessions[jj][0], "NO ANSWER"))'''
            
            temp_result = [] #Initialize list to store answers of each question
            for i in range(len(questions)):
                temp_result.append([]) #It is list of lists, each question has its own list of answers
            total_result = [] #When each question is finished, dictionify it and put it here
            
            j = 0 #I declare j here because I need it outside its loop
            pointer = 0 #location in result
            current_qid = result[0][0]
            
            # Correct way to make dictionairies
            for i in range(len(questions)):
                for j in range(len(sessions)):
                    #print("pointer = ", pointer)
                    #print("q = ", questions[i][0])
                    #print("s = ", sessions[j][0])
                    temp_result[i].append(dict(session = sessions[j][0], ans = result[pointer][2]))
                    pointer = pointer + 1
                total_result.append(dict(questionID = questions[i][0], answers = temp_result[i]))
            # The following block is replaced by block above
            '''for i in range(len(questions)):
                k = 0
                #pointer < len is new addition
                if (pointer < len(result) and result[pointer][0] == current_qid and pointer != 0):
                    pointer += 1
                    current_qid = result[pointer][0]
                #else:
                elif (pointer < len(result)):
                    current_qid = result[pointer][0]
                for j in range(len(sessions)):
                    if (pointer + k >= len(result) and k == len(sessions)):
                        break #Checked everything for this question, break
                    elif (pointer + k >= len(result) and k < len(sessions)):
                        while (k < len(sessions)): #Questions ended, but some NO ANSWERS must be appended
                            temp_result[i].append(dict(session = sessions[k][0], ans = "NO ANSWER"))
                            k += 1
                        break
                    #print(k)
                    if (k < len(sessions) and result[pointer + j][1] == sessions[k][0]): #Q has answer for current session
                        temp_result[i].append(dict(session = result[pointer + j][1], ans = result[pointer + j][2]))
                        k += 1
                    else: #Q does not have answer for current session, NO ANSWER
                        while (k < len(sessions) and result[pointer + j][1] != sessions[k][0]):
                            temp_result[i].append(dict(session = sessions[k][0], ans = "NO ANSWER"))
                            k += 1
                        j -= 1
                pointer += j
                total_result.append(dict(questionID = current_qid, answers = temp_result[i]))'''
            if (format == "json"):
                return jsonify({"questionnaireID": str(questionnaireID),
                "full_answers": total_result}), 200
            else:
                newDict = dict(questionnaireID = str(questionnaireID),
                full_answers = total_result)
                return generateCSVresponse(newDict, "full_answers")
        else:
            return jsonify({
                        "type":"/errors/authentication-error",
                        "title": "Unauthorized User",
                        "status": "401",
                        "detail":"User is unauthorized",
                        "instance":"/Users/getallanswers"}), 401

    if request.method == 'POST':
        return jsonify({"type": "/errors/operation-error",
                        "title": "Invalid method.",
                        "status": "405",
                        "detail": "POST is invalid in getallanswers.",
                        "instance": "/Users/getallanswers"}), 405
