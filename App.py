from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

engine = create_engine("mysql+pymysql://root:2326@127.0.0.1/userdata?charset=utf8mb4")

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    content = Column(String(200), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            session = Session()
            session.add(new_task)
            session.commit()
            session.close()
            return redirect('/')
        except:
            return "There was an issue adding the task"
    else:
        session = Session()
        tasks = session.query(Todo).order_by(Todo.date_created).all()
        session.close()
        return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
