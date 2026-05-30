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

def cmd_remove_copy(args, conn):
    with conn.cursor() as cursor:
        
        sql1 = "SELECT status FROM copy WHERE copy_id = %s"
        values = (args.id,)
        cursor.execute(sql1, values)
        check_copy = cursor.fetchone()




        if check_copy:
            if check_copy[0] != 'loaned':
                sql2 = "DELETE FROM copy WHERE copy_id = %s"
                cursor.execute(sql2, values)
                conn.commit()

                print(f"La cpia con ID: {args.id} fue eliminada con exito.")
            else:
                raise LibraryManagerError("No se puede eliminar la copia porque tiene status loaned.")
        else:
            raise LibraryManagerError(f"No hay una copia con ID: {args.id}.")