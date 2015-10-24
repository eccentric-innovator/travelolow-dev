from flask import Flask
from flask import views,render_template,request,session,flash,redirect,url_for
import datetime
import urllib2
import urllib
import json
#from flask.ext.wtf import Form
from wtforms import *
from wtforms.validators import *

app = Flask(__name__)
app.secret_key = 'Vict0ry'


class HELLO(views.MethodView):
    def get(self):
        return 'Hello Dude...'

class search(views.MethodView):
    def __init__(self):
        self.flights = [1,2,3]
        self.status  = True
    def get(self):
        return render_template('homepage.html')

    def post(self):
        source      = str(request.form['source'])
        destination = str(request.form['destination'])
        travel_date = datetime.datetime.strptime(str(request.form['date_from']), "%m/%d/%Y").strftime("%Y%m%d")
        adult_count = int(request.form['Adults'])
        self.status,self.flights = self.hit_api(source,destination,travel_date,adult_count)

        ##return('SOURCE: '+source+'\n'+'DESTINATION: '+destination+'\n'+'TRAVEL DATE:'+str(travel_date)+'\n'+'ADULT COUNT:'+str(adult_count) )
        if self.status == True:
            session['var'] = self.flights
            return str(self.flights)
        else:
            ##Need to add flashed message to the Template
            flash(self.flights[0]["Error"])
            return redirect(url_for('search'))


    def hit_api(self,SOURCE,DESTINATION,DOT,ADULT_COUNT=1,CHILDREN=0,INFANTS=0):
        ## SOURCE: SOURCE LOCATION TO START
        ## DESTINATION: DESTINATION LOCATION
        ## DOT: Date Of Travel

        app_id      = "563ae2b9"
        app_key     = "57848b14d881248a4f109d1630543ca9"
        base_url    = "http://developer.goibibo.com/api/"

        url         =  base_url + "search/" + "?app_id=" + app_id + "&app_key=" + app_key + "&format=json" + "&source=%s" % SOURCE + "&destination=%s" % DESTINATION + "&dateofdeparture="+ DOT +"&seatingclass=E,B" + "&adults=%d" % ADULT_COUNT + "&children=%d" % CHILDREN + "&infants=%d" % INFANTS
        req         =  urllib2.Request(url)
        f           =  urllib2.urlopen(req)
        res         =  json.loads(f.read())
        status      =  True

        if res["data_length"]==1:
            status = False
            flights = [
                {"Error":res["data"]["Error"]}
                      ]
            return status,flights
        else:
            flights =     [
                    {
                        "source":results["origin"],
                        "destination":results['destination'],
                        "flight_number":results['flightno'],
                        "airline":results['airline'],
                        "price":results['fare']['totalfare'],
                        "duration":results['splitduration'],
                        "onwardflight":[
                                         {
                                             "source":onward_flight["origin"],
                                             "destination":onward_flight["destination"],
                                             "flight_number":onward_flight["flightno"],
                                             "airline":onward_flight["airline"],
                                             "price":onward_flight["fare"]["totalfare"],
                                             "duration":onward_flight["splitduration"]
                                         }
                                         for onward_flight in results['onwardflights']
                                       ]
                    }
                    if results.has_key("onwardflights")
                    else
                    {
                        "source":results["origin"],
                        "destination":results['destination'],
                        "flight_number":results['flightno'],
                        "airline":results['airline'],
                        "price":results['fare']['totalfare'],
                        "duration":results['splitduration']
                    }
                    for results in res["data"]["onwardflights"]
                   ]


        return status,flights





app.add_url_rule('/hello',view_func=HELLO.as_view('HELLO'))
app.add_url_rule('/',view_func=search.as_view('search'))


if __name__ == '__main__':
	app.debug = True
	app.run()


