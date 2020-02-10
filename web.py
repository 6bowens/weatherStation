from flask import Flask, render_template

#init webserver
app = Flask(__name__)
@app.route("/")
def index():

   with open ('data.txt') as file:
      airTemp = file.readline()
      airHum = file.readline()
      waterTemp = file.readline()
      timeString = file.readline()
   file.close()


   templateData = {
      'time': timeString,
      'airHum': airHum,
      'airTemp': airTemp,
      'waterTemp': waterTemp
      }
   return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=2000, debug=True)

