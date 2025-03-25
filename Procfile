web: gunicorn -w 4 -b 0.0.0.0:5000 app:app
frontend: cd .. && npm install && npm run build && serve -s build
