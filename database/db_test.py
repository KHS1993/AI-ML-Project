import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
  raise RuntimeError("DATABASE_URL is not set")

print("DATABASE_URL found")

try:
  connection = psycopg2.connect(DATABASE_URL)

  print("PostgresSQL connection successful")

  cursor = connection.cursor()
  cursor.execute("SELECT 1")

  print("SELECT 1:", cursor.fetchone)

  cursor.close()
  connection.close()

except Exception as e:
  print("Connection failed:")
  print(type(e).__name__)
  print(e)