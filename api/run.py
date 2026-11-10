from app import create_app, preparar_banco

app = create_app()

if __name__ == "__main__":
    preparar_banco()
    app.run(host="0.0.0.0", port=5000, debug=True)
