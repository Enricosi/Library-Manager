import pymysql
from exceptions import LibraryManagerError


def cmd_add_user(args, conn):
    try:    
        with conn.cursor() as cursor:

            sql = "INSERT INTO library_user (username, first_name, last_name) VALUES (%s, %s, %s)"
            values = (args.username, args.first_name, args.last_name)
            cursor.execute(sql, values)
            conn.commit()

            print(f"El usuario {args.username} fue agregado con exito.")

    except pymysql.err.IntegrityError:
        conn.rollback()
        raise LibraryManagerError(f'El nombre de usuario {args.username} ya existe, elige otro por favor')


def cmd_remove_user(args, conn):
    with conn.cursor() as cursor:

        sql1 = "SELECT user_id FROM library_user WHERE username = %s"
        values1 = (args.username,)
        cursor.execute(sql1, values1)
        user_exist = cursor.fetchone()

        if user_exist:
            sql2 = "SELECT return_date FROM loan WHERE user_id = %s and return_date IS NULL"
            values2 = (user_exist[0],)
            cursor.execute(sql2, values2)

            active_loan = cursor.fetchone()

            if not active_loan:
                sql3 = "DELETE FROM library_user WHERE user_id = %s"
                cursor.execute(sql3, (user_exist[0],))
                conn.commit()

                print(f"El usuario: {args.username} fue eliminado con exito.")
            else:
                raise LibraryManagerError(f"No se pudo eliminar al usuario: {args.username} porque tiene prestamos activos.")
        else:
            raise LibraryManagerError(f"No existe el usuario {args.username}.")

def cmd_change_user_activity(args,conn):
    with conn.cursor() as cursor:

        username = args.user

        sql1 = "SELECT user_id FROM library_user WHERE username = %s"
        values1 = (username,)
        cursor.execute(sql1, values1)

        user_exist = cursor.fetchone()

        if user_exist:
                sql2 = "SELECT is_active FROM library_user WHERE user_id = %s"
                cursor.execute(sql2, (user_exist[0],))

                activity = cursor.fetchone()

                if activity[0]:
                    sql3 = "SELECT return_date FROM loan WHERE user_id = %s and return_date IS NULL"
                    cursor.execute(sql3, (user_exist[0],))
                    
                    active_loan = cursor.fetchone()
                    
                    if not active_loan:
                        sql4 = "UPDATE library_user SET is_active = NOT is_active WHERE user_id = %s"
                        cursor.execute(sql4, (user_exist[0],),)
                        conn.commit()

                        print(f"El estado de actividad del usuario: {username} se actualizo con exito.")
                    else:    
                        raise LibraryManagerError(f"No se puede cambiar el estado de actividad del usuario: {username} a inactivo porque tiene prestamos activos.")
                else:
                    sql5 = "UPDATE library_user SET is_active = NOT is_active WHERE user_id = %s"
                    cursor.execute(sql5, (user_exist[0],))
                    conn.commit()

                    print(f"El estado de actividad del usuario: {username} se actualizo con exito.")
        else:
            raise LibraryManagerError(f"El usuario: {username} no existe en la base de datos.")

def cmd_list_users(args, conn):
    with conn.cursor() as cursor:
        active = args.active if args.active else None
        inactive = args.inactive if args.inactive else None
        have_loans = args.have_loans if args.have_loans else None

        if active and inactive:
            raise LibraryManagerError("No puedes usar --active e --inactive al mismo tiempo.")

        conditions = []
        values = []

        if have_loans:
            sql = "SELECT u.user_id, u.username, u.first_name, u.last_name, u.is_active, COUNT(l.loan_id) AS cantidad_prestamos, u.created_at " \
                "FROM library_user u LEFT JOIN loan l ON l.user_id = u.user_id AND l.return_date IS NULL"
        else:
            sql = "SELECT user_id, username, first_name, last_name, is_active, created_at FROM library_user u"

        if active:
            conditions.append('u.is_active = %s')
            values.append(1)

        if inactive:
            conditions.append('u.is_active = %s')
            values.append(0)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        if have_loans:
            sql += " GROUP BY u.user_id HAVING COUNT(l.loan_id) > 0"

        cursor.execute(sql, values)

        lista = cursor.fetchall()

        if not lista:
            raise LibraryManagerError("No hay usuarios que mostrar o no coinciden con los filtros aplicados.")

        if have_loans:
            for u in lista:
                print(f"ID: {u[0]} | Username: {u[1]} | First Name: {u[2]} | Last Name: {u[3]} | Activity: {u[4]} | Cantidad de prestamos: {u[5]} | Created at: {u[6]}")
        else:
            for u in lista:
                print(f"ID: {u[0]} | Username: {u[1]} | First Name: {u[2]} | Last Name: {u[3]} | Activity: {u[4]} | Created at: {u[5]}")