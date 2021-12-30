from webapp import create_app

app = create_app()

# Execute the flask app only running this file
if __name__ == '__main__':
    # automatically rerun flask app every make change to the code 
    app.run(debug=True)