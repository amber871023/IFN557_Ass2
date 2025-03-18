# from mystoreapp import create_app

# if __name__ == '__main__':
#     napp = create_app()
#     napp.run(debug=True)

from mystoreapp import create_app

app = create_app()  # Initialize Flask app

# This is required for Vercel to handle requests
if __name__ == "__main__":
    app.run()  # Do not use debug=True for production

