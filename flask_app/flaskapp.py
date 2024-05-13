from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    if 'db_credentials' not in session:
        return None
    creds = session['db_credentials']
    return pymysql.connect(host='localhost', user=creds['user'], password=creds['password'], database=creds['database'])

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/connect', methods=['POST'])
def connect():
    user = request.form['username']
    password = request.form['password']
    database = request.form['database']
    try:
        conn = pymysql.connect(host='localhost', user=user, password=password, database=database)
        conn.close()
        session['db_credentials'] = {'user': user, 'password': password, 'database': database}
        return redirect(url_for('manage'))
    except pymysql.err.OperationalError as e:
        error_code, error_message = e.args
        if error_code == 1045:
            flash("Access denied: Incorrect username or password.", "error")
        elif error_code == 1049:
            flash("Error: Unknown database specified.", "error")
        else:
            flash(f"Database connection error: {error_message}", "error")
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "error")
    return redirect(url_for('index'))

@app.route('/manage')
def manage():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT people.IDPerson, people.IDCard, people.Lastname, people.Firstname, 
               site.Name AS SiteName, department.Name AS DepartmentName, people.IDSAP
        FROM people
        LEFT JOIN site ON people.Site = site.IDSite
        LEFT JOIN department ON people.Department = department.IDDepartment
    """)
    people = cursor.fetchall()
    conn.close()
    return render_template('manage.html', people=people)

@app.route('/add_person_form', methods=['GET'])
def add_person_form():
    # When first visiting the form, no data needs to be pre-populated.
    return render_template('add_person.html', data={})

@app.route('/add_person', methods=['POST'])
def add_person():
    form_data = {
        'id_card': request.form['id_card'],
        'lastname': request.form['lastname'],
        'firstname': request.form['firstname'],
        'site': request.form['site'],
        'department': request.form['department'],
        'idsap': request.form['idsap']
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    # Check for existing IDCard or IDSAP
    cursor.execute("SELECT * FROM people WHERE IDCard = %s OR IDSAP = %s", (form_data['id_card'], form_data['idsap']))
    if cursor.fetchone():
        flash('Error: IDCard or IDSAP already exists', 'error')
        conn.close()
        # Render the same form again with the data previously entered
        return render_template('add_person.html', data=form_data)

    try:
        cursor.execute("""
            INSERT INTO people (IDCard, Lastname, Firstname, Site, Department, IDSAP) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (form_data['id_card'], form_data['lastname'], form_data['firstname'], form_data['site'], form_data['department'], form_data['idsap']))
        conn.commit()
        flash('Person added successfully', 'success')
    except Exception as e:
        flash(f"Error adding person: {str(e)}", 'error')
    finally:
        conn.close()
    return redirect(url_for('manage'))


@app.route('/edit_person/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    conn = get_db_connection()
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people WHERE IDPerson = %s", (id,))
        person = cursor.fetchone()
        return render_template('edit_person.html', person=person)
    else:
        id_card = request.form['id_card']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        site = request.form['site']
        department = request.form['department']
        idsap = request.form['idsap']
        try:
            cursor.execute("""
                UPDATE people SET IDCard = %s, Lastname = %s, Firstname = %s, Site = %s, Department = %s, IDSAP = %s 
                WHERE IDPerson = %s
            """, (id_card, lastname, firstname, site, department, idsap, id))
            conn.commit()
            flash('Person updated successfully', 'success')
        except Exception as e:
            flash(f"Error updating person: {str(e)}", 'error')
        finally:
            conn.close()
        return redirect(url_for('manage'))

@app.route('/delete_person/<int:id>')
def delete_person(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM people WHERE IDPerson = %s", (id,))
        conn.commit()
        flash('Person deleted successfully', 'success')
    except Exception as e:
        flash(f"Error deleting person: {str(e)}", 'error')
    finally:
        conn.close()
    return redirect(url_for('manage'))

if __name__ == "__main__":
    app.run(debug=True)
