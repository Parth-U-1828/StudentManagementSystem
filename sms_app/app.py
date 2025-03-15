from flask import *
from sqlite3 import *

app = Flask(__name__)

@app.route("/")
def home():
	con = None
	try:
		con = connect("sms.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		return render_template("home.html",msg=data)
	except Exception as e:
		msg = "issue " + str(e)
		return render_template("home.html",msg=msg)
	finally:
		if con is not None:
			con.close()

@app.route("/create",methods=["GET","POST"])
def create():
	if request.method == "POST":
		rno = int(request.form["rno"])
		name = request.form["name"]
		marks = int(request.form["marks"])
		con = None
		try:
			con = connect("sms.db")
			cursor = con.cursor()
			sql = "insert into student values('%d','%s','%d')"
			cursor.execute(sql % (rno,name,marks))
			con.commit()
			msg = "Record Created Successfully !!"
			return render_template("create.html",msg=msg)
		except Exception as e:
			con.rollback()
			msg = "Issue " + str(e)
			return render_template("create.html",msg=msg)
		finally:
			if con is not None:
				con.close()
	else:
		return render_template("create.html")

@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
	con = None
	try:
		con = connect("sms.db")
		cursor = con.cursor()
		sql = "delete from student where rno = '%d'"
		cursor.execute(sql%(id))
		con.commit()
	except Exception as e:
		con.rollback()
		msg = "issue " + str(e)
		print(msg)
	finally:
		if con is not None:
			con.close()
	return redirect(url_for("home"))

if __name__ == "__main__":
	app.run(debug=True,use_reloader=True)
