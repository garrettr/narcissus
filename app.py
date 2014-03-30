#!/usr/bin/env python

from datetime import datetime

# http://flask.pocoo.org/docs/
from flask import Flask

# http://pythonhosted.org/Flask-SQLAlchemy/
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + '/tmp/db.sqlite'
db = SQLAlchemy(app)


class Mirror(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)
    scans = db.relationship('Scan', backref='mirror') # TODO: lazy='dynamic'?

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<Mirror %r>' % self.url


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mirror_id = db.Column(db.Integer, db.ForeignKey('mirror.id'))

    time_started = db.Column(db.DateTime)
    time_finished = db.Column(db.DateTime)

    passed = db.Column(db.Boolean, default=False)

    def __init__(self):
        time_started = datetime.utcnow()

    def __repr__(self):
        return '<Scan (%s) %r>' % ('PASS' if self.passed else 'FAIL',
                                   self.time_started)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
