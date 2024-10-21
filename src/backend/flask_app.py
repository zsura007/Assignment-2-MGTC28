from flask import Flask
import asyncio
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_utsc_students():
    return { "message" : "Hello MGTC28 Students" }

@app.route("/")
def hello_utsc_students():
    return { "message" : "Hello MGTC28 Students" }