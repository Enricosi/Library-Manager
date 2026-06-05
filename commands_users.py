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
                cursor.execute(sql3, user_exist[0],)
                conn.commit()

                print(f"El usuario: {args.username} fue eliminado con exito.")
            else:
                raise LibraryManagerError(f"No se pudo eliminar al usuario: {args.username} porque tiene prestamos activos.")
        else:
            raise LibraryManagerError(f"No existe el usuario {args.username}.")

