from flask import Flask, render_template, request, redirect
import sqlite3
import csv
import re
import random
from flaskapp.run_model import run_model
from flaskapp import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def sen2query():
    if request.method == 'POST':
        # result = request.form
        ### show table ###
        table_name = ""
        question = ""
        table_name = request.form['Table']
        question = request.form['Question']

        num_col = 0
        if table_name == 'table_election':
            header = ['District', 'Incumbent', 'Party', 'First_elected', 'Result', 'Candidates']
            num_col = 6
        elif table_name == 'table_mlb':
            header = ['Player', 'Position', 'School', 'Hometown', 'College']
            num_col = 5

        conn = sqlite3.connect("flaskapp/try")
        c = conn.cursor()
        rows = c.execute("SELECT * FROM " + table_name)
        table = []
        for row in rows:
            table.append(row)

        if question == "":
            return render_template("index.html", table_name=table_name, header=header, table=table)

        ### submit question ###
        # query_name = "Query not generated"
        query_name = run_model(question.lower())
        print("Query:", query_name)
        return render_template("index.html", table_name=table_name, question=question, query=query_name)

        conn1 = sqlite3.connect("flaskapp/test.db")
        c1 = conn1.cursor()
        rows1 = c1.execute(query_id)
        table = []
        for row in rows1:
            tmp = []
            if col_id != "":
                for i in range(0, col_id):
                    tmp.append("")
                tmp.append(row[0])
                for i in range(col_id + 1, num_col):
                    tmp.append("")
            table.append(tmp)

        return render_template("index.html", question=question, table_name=table_name, query=query_name,
                               header=header, table=table)
