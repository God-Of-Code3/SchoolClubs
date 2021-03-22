from flask import Flask, render_template, url_for


app = Flask(__name__)


def main():
    app.run()


@app.route('/')
@app.route('/index/')
def index():
    params = dict()
    params["title"] = "title"
    return render_template('index.html', **params)


if __name__ == '__main__':
    main()