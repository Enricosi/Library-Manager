import pymysql
from parser import parse_args
from dispatch import *
from connect import get_connection
from exceptions import LibraryManagerError



def main():
    """Entry point: parse arguments, open a DB connection, and dispatch the command.

    Connection errors (missing env vars, unreachable host) are caught before dispatch
    so the finally block never runs against an undefined conn.
    """
    args = parse_args()
    try:
        conn = get_connection()
    except(ValueError, pymysql.err.OperationalError) as e:
        print(e)
        return
    try:
        dispatch(args, conn)
    except (LibraryManagerError, RuntimeError) as e:
        print(e)
    finally:
        if conn.open:    
            conn.close()

if __name__ == '__main__':
    main()