from exceptions import LibraryManagerError
import datetime


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

def cmd_change_copy_status(args, conn):
    with conn.cursor() as cursor:

        VALID_TRANSACTIONS = {
            'available' : ['damaged', 'lost'],
            'loaned' : ['damaged', 'lost'],
            'damaged' : ['available', 'lost'],
            'lost' : ['available']
        }

        new_status = args.new_status


        sql1 = "SELECT copy_id FROM copy WHERE copy_id = %s"
        values1 = (args.copy,)
        cursor.execute(sql1, values1)

        copy_exist = cursor.fetchone()

        if copy_exist:
            sql2 = "SELECT status FROM copy WHERE copy_id = %s"
            cursor.execute(sql2, values1)

            current_status = cursor.fetchone()

            if new_status in VALID_TRANSACTIONS.get(current_status[0]):

                date = datetime.datetime.now()

                sql3 = "UPDATE copy SET status = %s WHERE copy_id = %s"
                
                if current_status[0] == 'loaned':
                    sql4 = "SELECT loan_id FROM loan WHERE copy_id = %s AND return_date IS NULL"
                    cursor.execute(sql4, values1)

                    loan_id = cursor.fetchone()
                    if loan_id:
                        sql5 = "UPDATE loan SET return_date = %s WHERE loan_id = %s"
                        values3 = (date, loan_id[0])
                        cursor.execute(sql5, values3)
                    else:
                        raise LibraryManagerError("Ha ocurrido un error al buscar el loan.")
                
                values2 = (new_status, args.copy)
                cursor.execute(sql3, values2)
                conn.commit()

                print("Status de la copia actualizado con exito")
            else:
                raise LibraryManagerError("Transaccion no permitida") 
        else:
            raise LibraryManagerError(f"La copia con ID: {args.copy} no existe en la base de datos.")

def cmd_list_copies(args, conn):
    with conn.cursor() as cursor:

        title = args.title if args.title else None
        status = args.status if args.status else None

        sql = "SELECT c.copy_id, b.title, c.status, c.shelf_location, c.created_at FROM copy c INNER JOIN book b ON c.book_id = b.book_id"

        conditions = []
        values = []

        if title:
            conditions.append('b.title LIKE %s')
            values.append(f"%{title}%")

        if status:
            conditions.append('c.status = %s')
            values.append(status)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        cursor.execute(sql, values)

        lista = cursor.fetchall()

        if lista:
            for i in lista:
                print(f"ID: {i[0]} | Title: {i[1]} | Status: {i[2]} | Shelf Location: {i[3]} | Created at: {i[4] or '-'}")
        else:
            print("No hay copias que mostrar.")