import pymysql
from exceptions import LibraryManagerError


def cmd_add_book(args, conn):
    try:
        with conn.cursor() as cursor:

            year = args.year if args.year else None
            isbn = args.isbn if args.isbn else None

            sql = "INSERT INTO book (title, author, genre, published_year, isbn) VALUES (%s, %s, %s, %s, %s)"
            
            values = (args.title, args.author, args.genre, year, isbn)

            cursor.execute(sql, values)
            conn.commit()
            print(f"El Libro {args.title} fue agregado con exito.")

    except pymysql.err.IntegrityError:
        conn.rollback()
        raise LibraryManagerError(f"El isbn introducido ya existe.")