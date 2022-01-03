# import flask
import re
from flask import Flask, render_template, request, redirect
from db import DB


# make flask object
app = Flask(__name__)

# get data
db = DB()


def get_data(item):
    return request.form[item]

#  get data of add student


def get_data_of_add():
    return get_data(item="stdid"), get_data(item="std_name"), get_data(item="std_depatment")


@app.route('/add_std', methods=['GET', 'POST'])
def add_std():
    massage = ""
    if request.method == 'POST':
        # get daa
        std_id, std_name, std_dept = get_data_of_add()
        if db.reigster_std(std_id=std_id, name=std_name, collage=std_dept):
            massage = "Success Added"
        else:
            massage = "Student Id is already found!!"

    return render_template('/add_std.html', massage=massage)


# student show
@app.route('/')
def std_show():
    rows = db.get_all()
    return render_template("/std_show.html", rows=rows, row_len=len(rows))


@app.route('/search_std', methods=['Get', 'POSt'])
def search_data():
    if request.method == 'POST':
        data, status = db.search_std(std_id=get_data(item="stdid"))
        if status:
            if len(data) > 0:
                return render_template('/std_update.html', data=data)
            else:
                return render_template('/search_std.html', massage='not exists')
        else:
            return render_template('/search_std.html', massage="error")
    else:
        return render_template('/search_std.html', massage='')

# get data of update student information


def get_data_of_update():
    return get_data(item="stdid"), get_data("std_name"), get_data("department")


# update route
@app.route("/std_update", methods=['GET', 'POST'])
def std_update():
    data = None
    if request.method == 'POST':
        std_id, new_name, new_dep = get_data_of_update()
        if db.update_std(std_id=std_id, name=new_name, collage=new_dep):
            data, status = db.search_std(std_id=std_id)
            return render_template('/std_update.html', data=data, massage='Success editing')
        else:
            return render_template('/std_update.html', data=data, massage='error')


@app.route("/delete_std/<student_id>", methods=['GET', 'POST'])
def std_delete(student_id):
    std_id = str(student_id).split('=')[1]
    if db.delete_std(std_id=std_id):
        return redirect('/')
    else:
        return render_template("/delete_std.html", massage='error deleted')


# run to appliction
if __name__ == "__main__":
    app.run(debug=True)
