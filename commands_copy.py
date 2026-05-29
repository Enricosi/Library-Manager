import pymysql
from exceptions import LibraryManagerError


def cmd_add_copy(args, conn):
        with conn.cursor() as cursor:

            book_id = args.book

            sql1 = "SELECT book_id FROM book WHERE book_id  = %s" 
            values1 = (book_id,)
            cursor.execute(sql1, values1)

            book_exist = cursor.fetchone()

            if book_exist:

                location = args.location if args.location else None

                sql2 = "INSERT INTO copy (book_id, shelf_location) VALUES (%s, %s)"
                values2 = (book_id, location)
                cursor.execute(sql2, values2)
                conn.commit()

                print("La copia se agrego con exito.")

            else:
                raise LibraryManagerError(f"No es posible agregar esta copia porque el libro con ID: {book_id} no se encuentra en la base de datos.")

