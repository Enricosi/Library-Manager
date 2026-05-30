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
    
def cmd_remove_book(args, conn):

    with conn.cursor() as cursor:

        sql1 = "SELECT book_id FROM book WHERE book_id = %s"
        values = (args.id,)
        cursor.execute(sql1, values)

        book_exist = cursor.fetchone()

        if book_exist:        
            sql2 = "SELECT copy_id FROM copy WHERE book_id = %s"
            cursor.execute(sql2, values)

            have_copies = cursor.fetchone()

            if not have_copies:
                sql3 = "DELETE FROM book WHERE book_id = %s"
                cursor.execute(sql3, values)
                conn.commit()
                
                print(f"El libro con ID: {args.id} fue eliminado con exito.")
            else:
                raise LibraryManagerError(f"No se puede eliminar el libro con ID: {args.id} porque tiene copias asignadas.")
        else:
            raise LibraryManagerError(f"No existe un libro con ID: {args.id}")

def cmd_list_book(args, conn):
    with conn.cursor() as cursor:

        title = args.title if args.title else None
        genre = args.genre if args.genre else None
        author = args.author if args.author else None

        sql = "SELECT book_id, title, author, genre, published_year, isbn, created_at FROM book"

        conditions = []
        values = []

        if title:
            conditions.append('title LIKE %s')
            values.append(f"%{title}%")

        if genre:
            conditions.append('genre LIKE %s')
            values.append(f"%{genre}%")

        if author:
            conditions.append('author LIKE %s')
            values.append(f"%{author}%")

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        cursor.execute(sql, values)

        lista = cursor.fetchall()

        if lista:
            for i in lista:
                print(f"ID: {i[0]} | Title: {i[1]} | Author: {i[2]} | Genre: {i[3]} | Published year: {i[4] or '-'} | ISBN: {i[5] or '-'} | Created at: {i[6]}")
        else:
            print("No hay libros para mostrar o no coinciden con los filtros aplicados.")

