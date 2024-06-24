import psycopg2

conn = psycopg2.connect("postgresql://tvdi_4yok_user:iDz6N7ysJOj9QZZwKCqwGX3McyBtqWkj@dpg-cpsd2ro8fa8c73955g8g-a.singapore-postgres.render.com/tvdi_4yok")
conn.close()