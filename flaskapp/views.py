from flask import Flask, render_template, request, redirect
import sqlite3
import csv
import re
import random
from flaskapp.run_model import run_model
from flaskapp import app
# app = Flask(__name__)

with open('flaskapp/tables/question_query.csv', 'r') as f:
    reader = csv.reader(f)
    q_q = list(reader)
print("shape of q_q", len(q_q), len(q_q[0]))

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
        if ("Player" in table_name or "player" in table_name or
            "Position" in table_name or 'position' in table_name):
            table_name = 'table_mlb'
        elif ("District" in table_name or "district" in table_name or
                "Party" in table_name or 'party' in table_name):
            table_name = 'table_election'

        num_col = 0
        if table_name == 'table_election':
            header = ['District', 'Incumbent', 'Party', 'First_elected', 'Result', 'Candidates']
            num_col = 6
        elif table_name == 'table_mlb':
            header = ['Player', 'Position', 'School', 'Hometown', 'College']
            num_col = 5
        else:
            table_name = "No such table"
            return render_template("index.html", table_name=table_name)

        conn = sqlite3.connect("flaskapp/try")
        c = conn.cursor()
        rows = c.execute("SELECT * FROM " + table_name)
        table = []
        for row in rows:
            table.append(row)

        if question == "":
            return render_template("index.html", table_name=table_name, header=header, table=table)

        ### submit question ###
        query_name = ""
        col_id = ""
        for line in q_q:
            if question.lower() in line[1].lower():
                query_id = line[2]
                query_name = line[4]
                col_id = line[3]
                col_id = int(re.findall('\d+', col_id)[0])
                print("Question: ", question)
                break
        if query_name == "":
            question_words = re.sub(r'[^\w\s]', '', question)
            word_list = question_words.lower().split()
            ran_idx = random.randint(0, len(word_list) - 1)
            for line in q_q:
                if word_list[ran_idx] in line[1].lower():
                    query_id = line[2]
                    query_name = line[4]
                    col_id = line[3]
                    col_id = int(re.findall('\d+', col_id)[0])
                    print("Question: ", question)
                    break
        if query_name == "":
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
