from flask import Flask, render_template

app=Flask(__name__)
todos = [
    ("Get Milk",False),
    ("Learn programming", True),
    ("Tell Bailee she is the bestest wife ever", True)
    
]

@app.route("/")
def todo():
    return render_template("home.html", todos=todos)

@app.route("/<string:todo>")
def todo_item(todo: str):
    for text, completed in todos:
        if text.lower() == todo.lower(): 
            completed_text = "[x]" if completed else "[]"
            title = f"{completed_text} - Todos"
            return render_template("todo.html", text=text, completed=completed,title=title)
    return render_template("not-found.html", text=todo,title="Not found")
