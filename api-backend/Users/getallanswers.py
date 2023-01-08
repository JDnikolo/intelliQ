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
            FROM Answer INNER JOIN qoption
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
            
            temp_result = [] #Initialize list to store answers of each question
            for i in range(len(questions)):
                temp_result.append([]) #It is list of lists, each question has its own list of answers
            total_result = [] #When each question is finished, dictionify it and put it here
            
            j = 0 #I declare j here because I need it outside its loop
            pointer = 0 #location in result
            current_qid = result[0][0]
            for i in range(len(questions)):
                k = 0
                if (result[pointer][0] == current_qid and pointer != 0):
                    pointer += 1
                    current_qid = result[pointer][0]
                else:
                    current_qid = result[pointer][0]
                for j in range(len(sessions)):
                    if (pointer + k >= len(result) and k == len(sessions)):
                        break #Checked everything for this question, break
                    elif (pointer + k >= len(result) and k < len(sessions)):
                        while (k < len(sessions)): #Questions ended, but some NO ANSWERS must be appended
                            temp_result[i].append(dict(session = sessions[k][0], ans = "NO ANSWER"))
                            k += 1
                        break
                    if (result[pointer + j][1] == sessions[k][0]): #Q has answer for current session
                        temp_result[i].append(dict(session = result[pointer + j][1], ans = result[pointer + j][2]))
                        k += 1
                    else: #Q does not have answer for current session, NO ANSWER
                        while (k < len(sessions) and result[pointer + j][1] != sessions[k][0]):
                            temp_result[i].append(dict(session = sessions[k][0], ans = "NO ANSWER"))
                            k += 1
                        j -= 1
                pointer += j
                total_result.append(dict(questionID = current_qid, answers = temp_result[i]))
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
