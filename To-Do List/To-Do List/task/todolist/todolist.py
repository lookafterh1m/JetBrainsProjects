import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())


def all_tasks(session):
    rows = session.query(Table).all()
    tasks_todo = ""
    if rows:
        temp = {row.deadline: row.task for row in rows}
        sorted_rows = list(temp.keys())
        sorted_rows.sort()
        for i, row in enumerate(sorted_rows):
            tasks_todo += f"{i + 1}. {temp[row]}. {datetime.strftime(row, '%d %b')}\n"
        return tasks_todo
    return "Nothing to do!\n"


def today_tasks(session):
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    string = datetime.strftime(datetime.today(), "Today %d %b:\n")
    if rows:
        for i, row in enumerate(rows):
            string += f"{i + 1}. {row.task}\n"
        return string
    return string + "Nothing to do!\n"


def week_tasks(session):
    today = datetime.today()
    tasks = "\n"
    for i in range(7):
        day = today + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline == day.date()).all()
        tasks += datetime.strftime(day, "%A %d %b\n")
        if rows:
            for j, row in enumerate(rows):
                tasks += f"{j + 1}. {row.task}\n"
            tasks += row.task
        else:
            tasks += "Nothing to do!"
        tasks += '\n\n' if i != 6 else '\n'
    return tasks


def missed_tasks(session):
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    missed = "Missed tasks:\n"
    if rows:
        temp = {row.deadline: row.task for row in rows}
        sorted_rows = list(temp.keys())
        sorted_rows.sort()
        for i, row in enumerate(sorted_rows):
            missed += f"{i + 1}. {temp[row]}. {datetime.strftime(row, '%d %b')}\n"
        return missed
    return "All tasks:\nNothing is missed!\n"


def add_task(session, new_task: str, deadline: str):
    new_row = Table(task=new_task, deadline=datetime.strptime(deadline, "%Y-%m-%d").date())
    session.add(new_row)
    session.commit()


def delete_task(session, str_row):
    str_row = str_row.split('. ')
    task = str_row[1]
    rows = session.query(Table).filter(Table.task == task).all()
    if rows:
        session.delete(rows[0])
    session.commit()


def user_menu():
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()
    while True:
        choice = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n"
                       "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n")
        if choice == '1':
            print('\n' + today_tasks(session))
        elif choice == '2':
            print(week_tasks(session))
        elif choice == '3':
            print("All tasks:\n")
            print(all_tasks(session))
        elif choice == '4':
            print(missed_tasks(session))
        elif choice == '5':
            add_task(session, input("\nEnter task\n"), input("Enter deadline\n"))
            print("The task has been added!\n")
        elif choice == '6':
            all = all_tasks(session)
            print("Choose the number of the task you want to delete\n" + all)
            number = int(input())
            delete_task(session, all.split('\n')[number - 1])
            print("The task has been deleted!\n")
        else:
            if choice == '0':
                print("\nBye!")
            sys.exit()


user_menu()
