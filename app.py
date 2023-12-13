from flask import Flask, render_template, request, redirect, url_for,session
import dbconnect
import weatherdata

app = Flask(__name__)
app.secret_key = "alphanumerickeydata"

objconn = dbconnect.getconnection()
cursor = objconn.cursor()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html',username=session['username'])
    else:
        return render_template('home.html')
    
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        pwd=request.form['password']
        try:
            cursor.execute("select username,password from users where username= %s", (username,))
            user=cursor.fetchone()            
            if user and pwd == user[1]:
                session["username"]=user[0]
                return redirect(url_for('home'))
            else:
                return render_template('login.html',error="Invalid username or password")
        except Exception  as e:
                return render_template('login.html',error="An error occurred: " + str(e))                            
    return render_template('login.html')        
        
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        useremail = request.form['email']
        pwd = request.form['password']
        cursor.execute("insert into users(username,useremail,password) VALUES (%s, %s, %s)",(username, useremail, pwd))  
        objconn.commit()
        return redirect(url_for("login")) 
    return render_template('register.html')

@app.route('/weatherurl',methods=['GET', 'POST'])
def weatherurl():
    if request.method == 'POST':
        try:
            cityname = request.form.get('cityname')
            #print("City Name:", cityname)
            citykey=weatherdata.getLocation(cityname)
            forecast=weatherdata.getforecast(citykey)    
            strmaxtemp=forecast[0]['Temperature']['Maximum']['Value']
            strmintemp=forecast[0]['Temperature']['Minimum']['Value']
            strdayforecast=forecast[0]['Day']['IconPhrase']
            strnightforecast=forecast[0]['Night']['IconPhrase']
            cursor.execute("SELECT * FROM weatherdata WHERE cityname = %s", (cityname,))
            if cursor.rowcount == 0:
                cursor.execute("insert into weatherdata(citykeyid,cityname,tempmin,tempmax,dayforecast,nightforecast) VALUES (%s, %s, %s, %s, %s, %s)",(citykey,cityname,strmaxtemp,strmintemp,strdayforecast,strnightforecast))  
                objconn.commit()
            return render_template('weather.html', forecast=forecast,cityname=cityname)
        except Exception  as e:
            return render_template('weather.html', error="An error occurred: ",cityname=cityname)
    else:
        return render_template('weather.html')

@app.route('/searched')
def searched():
    cursor = objconn.cursor()  # Assuming 'objconn' is your database connection object
    cursor.execute("SELECT * FROM weatherdata")  # Replace 'your_table_name' with your actual table name
    records = cursor.fetchall()  # Fetch all records from the table
    
    if records:
           print("Data fetched successfully")
    else:
           print("No data fetched")
    return render_template('searched.html', records=records)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')


if __name__ == '__main__':
    app.run(debug=False)
