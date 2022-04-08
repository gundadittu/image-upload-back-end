from app import create_app, db

app = create_app()

with app.app_context():
  db.create_all()
  db.session.commit()

app.run(host='0.0.0.0', port=8080)