from flask import Flask
app = Flask(__name__)
import random

random_number = random.randint(0, 9)

@app.route('/')
def hello_world():
    return '<h1>Guess a number between 0 and 9<h1>' \
           '<iframe src="https://www.behance.net/embed/project/22571611?ilo0=1" height="316" width="404" allowfullscreen lazyload frameborder="0" allow="clipboard-write" refererPolicy="strict-origin-when-cross-origin"></iframe>'


@app.route('/<int:number>')
def game(number):
    bool = True
    while bool:
        if number > random_number:
            return '<h1>Too high, try again!<h1>'
        if number < random_number:
            return '<h1>Too low, try again!<h1>'
        if number == random_number:
            bool = False
            return '<h1>You found me!<h1>'



if __name__ == '__main__':
    app.run(debug=True)
