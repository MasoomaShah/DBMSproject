from website import create_app
import psycopg2
from config import config

params = config()
conn = psycopg2.connect(**params)

app=create_app()

if __name__=='__main__':
    app.run(debug=True)#automatically reruns the server
    


