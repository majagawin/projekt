from sqlalchemy import create_engine, text

if __name__ == '__main__':
    engine = create_engine('postgresql://maja:maja@localhost:5432/baza')
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM public.Ogloszenia"))
        print(result.fetchall())
