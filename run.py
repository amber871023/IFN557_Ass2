# from mystoreapp import create_app

# if __name__ == '__main__':
#     napp = create_app()
#     napp.run(debug=True)

from mystoreapp import create_app

# Create the Flask app instance
app = create_app()

# Vercel requires a `handler` function
def handler(request, *args, **kwargs):
    return app(request.environ, start_response)

if __name__ == "__main__":
    app.run(debug=True)
