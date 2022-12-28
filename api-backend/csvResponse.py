import csv
from io import StringIO
from flask import Response
# Generates a Response for returning a CSV file from the contents
# of  JSON-like dictionary mainDict. 
# listKey: If mainDict contains a list of dicts, listKey can be the key of said list, 
# in order to add the nested dict keys to the CSV header.
# filename: the name of the file to be returned by the response.
def generateCSVresponse(mainDict:dict,listKey:str=None,filename:str="result.csv"):
    def generate():
        data = StringIO()
        w = csv.writer(data)
        mainKeys = list(mainDict.keys())
        mainCount=len(mainKeys)
        listOfDicts=[]
        if listKey!=None:
            listOfDicts=mainDict.pop(listKey)
            listKeys=list(listOfDicts[0].keys())
            mainKeys = list(mainDict.keys())
            mainCount=len(mainKeys)
            mainKeys.extend(listKeys)
        w.writerow(mainKeys)
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        w.writerow(mainDict.values())
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        padding = [None for i in range(mainCount)]
        for item in listOfDicts:
            towrite = padding.copy()
            towrite.extend(item.values())
            w.writerow(towrite)
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)
    response = Response(generate(), mimetype='text/csv')
    response.headers.set("Content-Disposition",
                            "attachment", filename=filename)
    return response