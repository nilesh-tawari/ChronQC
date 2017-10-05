from bottle import hook, response, route, run
import os.path as op
import sqlite3
import pandas as pd
from datetime import date
import sys

def main(args):
    # Parameters
    port = 8000
    if args.port is not None:
        if not len(args.port) == 4:
            print('Please use Four digit integer value for the port e.g. 8000')
            sys.exit(1)
        try:
            port = int(args.port)
        except:
            print('Please use Four digit integer value for the port e.g. 8000')
            sys.exit(1)
    ###############################################################################

    '''Run Annotations'''
    print (op.dirname(__file__))
    db = op.abspath(op.join(op.dirname(__file__), 'db','chronqc.annotations.db'))
    connection = sqlite3.connect(db)
    mycursor = connection.cursor()
    curr = mycursor.execute('''SELECT Run, Panel, Status, Annotation, GraphID, Date1, Date2 from Run_Annotations''')
    anndata = curr.fetchall()
    anndata = pd.DataFrame(anndata)
    anndata.rename(columns={0: "Run", 1: "Panel", 2: "Annotation"}, inplace=True)



    ###############################################################################

    '''Date Annotations'''
    curr = mycursor.execute('''SELECT Annotated_date, Notes, Panel FROM Date_Annotations''')
    datedata = curr.fetchall()
    connection.commit()
    datedata = pd.DataFrame(datedata)
    datedata.rename(columns={0: "Annotated_date", 1: "Notes", 2: "Panel"}, inplace=True)
    #datedata["Annotated_date"] = pd.to_datetime(datedata.Annotated_date, dayfirst=True)


    ###############################################################################
    # These lines are needed for avoiding the "Access-Control-Allow-Origin" errors

    @hook('after_request')
    def enable_cors():
        response.headers['Access-Control-Allow-Origin'] = '*'

    ###############################################################################
    # If you have to send parameters, the right sintax is as calling the resoure
    # with a kind of path, with the parameters separed with slash ( / ) and they
    # MUST to be written inside the lesser/greater than signs  ( <parameter_name> )
    '''Update Run Annotations '''

    @route('/dataQuery/<Runname>/<Panel>/<status>/<chartid>/<startdate>/<enddate>/<annotation>')
    def myQuery(Runname, Panel, status, chartid,startdate,enddate,annotation):
        print("Enter")
        todate = date.today().strftime('%Y-%m-%d')
        annotation = '{0} : {1}'.format(todate, annotation)
        try:
            mycursor.execute("UPDATE Run_Annotations SET Annotation = Annotation || '<br>' || ? , Status = ?, GraphID = ?, Date1 = ?, Date2 = ? WHERE Run = ? and Panel = ?;", (annotation,status,chartid,startdate,enddate,Runname,Panel))
        except:
            mycursor.execute("UPDATE Run_Annotations SET Annotation = Annotation || '<br>' || ? , Status = ?, GraphID = ?, Date1 = ?, Date2 = ? WHERE Run = ? and Panel = ?;", (annotation.decode("utf-8"),status,chartid,startdate,enddate,Runname,Panel))        
        connection.commit()
        print(mycursor.rowcount, " rows")
        if mycursor.rowcount == 0:
            try:
                mycursor.execute("Insert into Run_Annotations (Annotation, Run, Panel, Status, GraphID, Date1, Date2) values(?,?,?,?,?,?,?);", (annotation, Runname, Panel, status,chartid,startdate,enddate))
            except:    
                mycursor.execute("Insert into Run_Annotations (Annotation, Run, Panel, Status, GraphID, Date1, Date2) values(?,?,?,?,?,?,?);", (annotation.decode("utf-8"), Runname, Panel, status,chartid,startdate,enddate))
            connection.commit()
        return

    ###############################################################################
    '''Update Date Annotations'''

    @route('/datedataQuery/<Date>/<Panel>/<Notes>')
    def myDateQuery(Date, Panel, Notes):
        try:
            mycursor.execute('''INSERT INTO Date_Annotations (Annotated_date, Notes, Panel) VALUES (?,?,?);''', (Date, Notes,Panel))
        except:
            mycursor.execute('''INSERT INTO Date_Annotations (Annotated_date, Notes, Panel) VALUES (?,?,?);''', (Date, Notes.decode("utf-8"),Panel))
        connection.commit()
        return

    ###############################################################################
    '''get run annotation data'''

    @route('/runannotation')
    def runannotation():
        curr = mycursor.execute('''SELECT Run, Panel, Status, Annotation, GraphID, Date1, Date2 from Run_Annotations''')
        anndata = curr.fetchall()
        connection.commit()
        anndata = pd.DataFrame(anndata)
        anndata.rename(columns={0: "Run", 1:"Panel", 2: "Status", 3: "Annotation", 4: "GraphID", 5: "Date1", 6: "Date2"},inplace=True)
        runannotation = anndata.to_json(orient="records")
        return runannotation

    ###############################################################################
    '''get date annotation data'''

    @route('/dateannotation')
    def dateannotation():
        curr = mycursor.execute('''SELECT Annotated_date, Notes, Panel FROM Date_Annotations''')
        datedata = curr.fetchall()
        connection.commit()
        datedata = pd.DataFrame(datedata)
        datedata.rename(columns={0: "Annotated_date", 1: "Notes", 2: "Panel"}, inplace=True)
        #datedata["Annotated_date"] = pd.to_datetime(datedata.Annotated_date, dayfirst=True)
        dateannotation = datedata.to_json(orient="records")
        return dateannotation

    ###############################################################################
    run(host='localhost', port=port)
    # And the MOST important line to set this program as a web service is this
    # run(host=socket.gethostname(), port=8001)
