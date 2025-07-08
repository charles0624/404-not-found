from flask import Flask, render_template

app = Flask(__name__)

@app.route('/main_page')
def mainPage():
    return render_template('main_page.html')

@app.route('/question_editor')
def questionEditor():
    return render_template('question_editor.html')

@app.route('/game_board')
def gameBoard():
    return render_template('game_board.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
