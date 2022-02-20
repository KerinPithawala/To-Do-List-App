from turtle import title
from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskLlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"

@app.route('/',methods=['GET','POST'])
def hello():
    if request.method=='POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        new_task = Todo(title=title, desc=desc)
        db.session.add(new_task)
        db.session.commit()

    
    allTodo = Todo.query.all()
    
    return render_template('index.html', allTodo=allTodo)
   
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form.get('title')
        desc=request.form.get('desc')
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

