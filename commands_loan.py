from exceptions import LibraryManagerError
import datetime
import pymysql

def cmd_loan_copy(args, conn):
    with conn.cursor() as cursor:

        date = datetime.datetime.now()
        due_date = date + datetime.timedelta(days=args.days)
        
        sql1 = "SELECT status FROM copy WHERE copy_id = %s"
        values1 = (args.id,)
        cursor.execute(sql1,values1)

        copy_exist = cursor.fetchone()

        if not copy_exist:
            raise LibraryManagerError(f"No existe la copia con ID: {args.id}")

        if copy_exist[0] == 'available':
            sql2 = "SELECT user_id FROM library_user WHERE username = %s"
            values2 = (args.username,)
            cursor.execute(sql2, values2)

            user_exist = cursor.fetchone()
            
            if user_exist:
                sql3 = "SELECT is_active FROM library_user WHERE user_id = %s"
                values3 = (user_exist[0],)
                cursor.execute(sql3, values3)

                user_active = cursor.fetchone()

                if user_active[0]:
                    sql4 = "INSERT INTO loan (copy_id, user_id, loan_date, due_date) VALUES (%s, %s, %s, %s)"
                    values4 = (args.id, user_exist[0], date, due_date)
                    
                    sql5 = "UPDATE copy SET status = 'loaned' WHERE copy_id = %s "
                    values5 = (args.id,)
                    
                    cursor.execute(sql4, values4)
                    cursor.execute(sql5, values5)
                    conn.commit()

                    print("El prestamo se realizo con exito.")
                else:
                    raise LibraryManagerError(f"El usuario: {args.username} se encuentra inactivo.")
            else:
                raise LibraryManagerError(f"El usuario: {args.username} no existe en la base de datos.")
        else:
            raise LibraryManagerError(f"La copia con ID: {args.id} no se encuentra disponible")

def cmd_return_copy(args,conn):
    with conn.cursor() as cursor:

        date = datetime.datetime.now()

        sql1 = "SELECT status FROM copy WHERE copy_id = %s"
        values1 = (args.copy,)
        cursor.execute(sql1, values1)

        copy_exist = cursor.fetchone()

        if copy_exist:
            status = copy_exist[0]

            if status != 'loaned':
                raise LibraryManagerError(f"La copia con ID: {args.copy} no esta en prestamo.")
            else:
                sql2 = "UPDATE loan SET return_date = %s WHERE copy_id = %s AND return_date IS NULL"
                values2 = (date, args.copy) 
                
                sql3 = "UPDATE copy SET status = 'available' WHERE copy_id = %s"
                values3 = (args.copy,)

                cursor.execute(sql2, values2)
                cursor.execute(sql3, values3)
                conn.commit()

                print(f"El prestamo de la copia con ID: {args.copy} se cerro con exito.")
        else:
            raise LibraryManagerError(f"La copia con ID: {args.copy} no existe en la base de datos.")

def cmd_list_loans(args, conn):
    with conn.cursor() as cursor:

        active = args.active if args.active else None
        historical = args.historical if args.historical else None

        sql = "SELECT loan_id, copy_id, user_id, loan_date, due_date, return_date FROM loan"

        conditions = []

        if active and historical:
            raise LibraryManagerError("No puedes aplicar --active y --historical al mismo tiempo.")
        
        if active:
            conditions.append("return_date IS NULL")
        
        if historical:
            conditions.append("return_date IS NOT NULL")

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        cursor.execute(sql)

        lista = cursor.fetchall()

        if lista:
            for l in lista:
                print(f"Loan ID: {l[0]} | Copy ID: {l[1]} | User ID: {l[2]} | Loan Date: {l[3]} | Due Date: {l[4]} | Return Date: {l[5] or '-'}")
        else:
            raise LibraryManagerError("No hay loans que mostrar.")