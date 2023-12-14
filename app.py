from flask import Flask, render_template, request, redirect, url_for, session
import dbconnect  # Custom module to connect to the database.
import weatherdata  # Custom module to fetch weather data.

app = Flask(__name__)  # Initialize the Flask application.
app.secret_key = "alphanumerickeydata"  # Set a secret key for session data encryption.

objconn = dbconnect.getconnection()  # Get database connection from dbconnect module.
cursor = objconn.cursor()  # Create a cursor object to interact with the database.

@app.route('/')  # Define the route for the home page.
def home():
    # Check if a user is logged in by checking the session.
    if 'username' in session:
        # If logged in, render the home page with the username.
        return render_template('home.html', username=session['username'])
    else:
        # If not logged in, render the home page without the username.
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])  # Define the route for the login page.
def login():
    if request.method == 'POST':
        # Handle the POST request for login.
        username = request.form['username']
        pwd = request.form['password']
        try:
            # Query the database for the user.
            cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()            
            # Check if the user exists and the password matches.
            if user and pwd == user[1]:
                # Set the session with the username.
                session["username"] = user[0]
                return redirect(url_for('home'))
            else:
                # Return an error message if login is invalid.
                return render_template('login.html', error="Invalid username or password")
        except Exception as e:
            # Handle any exceptions during login.
            return render_template('login.html', error="An error occurred: " + str(e))                            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])  # Define the route for registration.
def register():
    if request.method == 'POST':
        # Handle the POST request for registration.
        username = request.form['username']
        useremail = request.form['email']
        pwd = request.form['password']
        # Insert the new user into the database.
        cursor.execute("INSERT INTO users(username, useremail, password) VALUES (%s, %s, %s)", (username, useremail, pwd))  
        objconn.commit()
        return redirect(url_for("login")) 
    return render_template('register.html')

@app.route('/weatherurl', methods=['GET', 'POST'])  # Define the route for weather information.
def weatherurl():
    if request.method == 'POST':
        try:
            cityname = request.form.get('cityname')
            citykey = weatherdata.getLocation(cityname)  # Get the location key for the city from the weatherdata module.
            forecast = weatherdata.getforecast(citykey)  # Get the weather forecast from the weatherdata module.
            # Extract relevant data from the forecast.
            strmaxtemp = forecast[0]['Temperature']['Maximum']['Value']
            strmintemp = forecast[0]['Temperature']['Minimum']['Value']
            strdayforecast = forecast[0]['Day']['IconPhrase']
            strnightforecast = forecast[0]['Night']['IconPhrase']
            # Check if the city data already exists in the database.
            cursor.execute("SELECT * FROM weatherdata WHERE cityname = %s", (cityname,))
            if cursor.rowcount == 0:
                # If not, insert the new weather data.
                cursor.execute("INSERT INTO weatherdata(citykeyid, cityname, tempmin, tempmax, dayforecast, nightforecast) VALUES (%s, %s, %s, %s, %s, %s)", (citykey, cityname, strmaxtemp, strmintemp, strdayforecast, strnightforecast))  
                objconn.commit()
            return render_template('weather.html', forecast=forecast, cityname=cityname)
        except Exception as e:
            # Handle any exceptions during fetching weather data.
            return render_template('weather.html', error="An error occurred: ", cityname=cityname)
    else:
        return render_template('weather.html')

@app.route('/searched')  # Define the route for displaying searched records.
def searched():
    cursor = objconn.cursor()
    cursor.execute("SELECT * FROM weatherdata")  # Fetch all records from the weatherdata table.
    records = cursor.fetchall()
    if records:
        print("Data fetched successfully")
    else:
        print("No data fetched")
    return render_template('searched.html', records=records)

@app.route('/logout')  # Define the route for logout.
def logout():
    session.pop('username', None)  # Remove the username from the session.
    return redirect(url_for('home'))

@app.route('/contactus')  # Define the route for the contact us page.
def contactus():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=False)  # Run the Flask application.
