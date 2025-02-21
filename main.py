from backend import create_app
#importng from the backend file and calling teh create application

app = create_app()

#if we run we run the web server, Entry point
if __name__ == '__main__':
    app.run(debug=True)