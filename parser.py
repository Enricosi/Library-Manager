import argparse

def valid_days(days):
    """Convert and validate the 'days' argument for loan_copy.

    Raises argparse.ArgumentTypeError if the value is not an integer
    between 1 and 60.
    """
    value = int(days)

    if value < 1 or value > 60:
        raise argparse.ArgumentTypeError("--days debe estar entre 1 y 60.")

    return value

def parse_args():
    """Parse CLI arguments for the Library Manager.

    Subcommands:
        add_book            Add a book (title, author, genre). Optional: -y/--year, -n/--isbn.
        remove_book         Remove a book by ID, only if it has no copies.
        list_book           List books. Optional filters: -t/--title, -g/--genre, -a/--author.
        add_copy            Add a physical copy of a book by book ID. Optional: -l/--location.
        remove_copy         Remove a copy by ID, only if its status is not 'loaned'.
        change_copy_status  Change a copy's status (damaged | lost | available). Cannot set 'loaned' here;
                             closes the active loan automatically if the copy was 'loaned'.
        list_copies         List copies. Optional filters: -t/--title, -s/--status.
        add_user            Register a user (username, first_name, last_name).
        remove_user         Remove a user by username, only if they have no active loans.
        change_user_activity  Toggle a user's is_active flag by username.
        list_users          List users. Optional flags: -a/--active, -i/--inactive, -l/--have_loans.
        loan_copy           Loan a copy (by ID) to a user (by username) for 1-60 days.
        return_copy         Close the active loan for a copy by copy ID.
        list_loans          List loans. Optional flags: -a/--active, -t/--historical.

    Returns:
        argparse.Namespace: Parsed arguments with 'command' set to the chosen subcommand.
    """
    parser = argparse.ArgumentParser(description="Library Manager CLI")

    subparsers = parser.add_subparsers(dest='command')

    add_book_parser = subparsers.add_parser('add_book', help="Agrega un libro a la base de datos." )
    add_book_parser.add_argument('title', help="Titulo del libro.")
    add_book_parser.add_argument('author', help="Nombre del autor del libro.")
    add_book_parser.add_argument('genre', help="Genero del libro.")
    add_book_parser.add_argument('-y', '--year', help="Fecha de publicacion del libro.")
    add_book_parser.add_argument('-n', '--isbn', help="International Standard Book Number.")

    remove_book_parser = subparsers.add_parser('remove_book', help="Elimina un libro de la base de datos siempre que no tenga copias con estatus loan.")
    remove_book_parser.add_argument('id', type=int, help="ID del libro que sera eliminado.")
    
    list_book_parser = subparsers.add_parser('list_book', help="Muestra todos los libros segun los filtros aplicados.")
    list_book_parser.add_argument('-t', '--title', help="Muesta si existe el libro con ese titulo.")
    list_book_parser.add_argument('-g', '--genre', help="Muestra los libros del genero especificado.")
    list_book_parser.add_argument('-a', '--author', help="Muestra los libros del autor especificado")

    add_copy_parser = subparsers.add_parser('add_copy', help="Agrega una copia fisica de un libro existente en la base de datos.")
    add_copy_parser.add_argument('book', type =int, help="ID del libro al que se le quiere crear una copia.")
    add_copy_parser.add_argument('-l', '--location', help="Indica la shelf location de la copia en la tienda.")

    remove_coy_parser = subparsers.add_parser('remove_copy', help="Elimina una copia de un libro debe tener un status distinto a loan.")
    remove_coy_parser.add_argument('id', type=int, help="ID de la copia que se va a eliminar.")

    change_copy_status_parser = subparsers.add_parser('change_copy_status', help="Cambia el status de una copy pero no puede cambiarlo a loaned.")
    change_copy_status_parser.add_argument('copy', type=int, help="ID de la copy a modificar")
    change_copy_status_parser.add_argument('new_status', choices=['damaged', 'lost', 'available'], help="Posibles ststus que puede tener una copy si se cambia desde este comando.Reglas: available → damaged, lost | loaned  → damaged, lost  (cierra el loan automáticamente) | damaged → available, lost | lost → available |")
    
    list_copies_parser = subparsers.add_parser('list_copies', help="Muestra las copias existentes segun los filtros aplicados")
    list_copies_parser.add_argument('-t', '--title', help="Filtra las copias por titulo.")
    list_copies_parser.add_argument('-s', '--status', choices=['available', 'loaned', 'damaged', 'lost'], help="Filtra las copias por estado.")
    
    add_user_parser = subparsers.add_parser('add_user', help="Agrega un nuevo usuario a la base de datos.")
    add_user_parser.add_argument('username', help="Username del user.")
    add_user_parser.add_argument('first_name', help="Primer nombre del user.")
    add_user_parser.add_argument('last_name', help="Apellido del user.")

    remove_user_parser = subparsers.add_parser('remove_user', help="Elimina un usuario de la base de datos si no tiene ningun loan activo.")
    remove_user_parser.add_argument('username', help="Username del user que se quiere eliminar.")

    change_user_activity_parser = subparsers.add_parser('change_user_activity', help="Cambia el estado de actividad de un usuario (activo/inactivo).")
    change_user_activity_parser.add_argument('user', help="Username del usuario a cambiar de estado.")

    list_users_parser = subparsers.add_parser('list_users', help="Muestra los usuarios existentes segun los filtros aplicados.")
    list_users_parser.add_argument('-a', '--active', action='store_true', help="Filtra por usuarios activos.")
    list_users_parser.add_argument('-i', '--inactive', action='store_true', help="Filtra por usuarios inactivos.")
    list_users_parser.add_argument('-l', '--have_loans', action='store_true', help="Filtra por usuarios que tienen prestamos activos.")

    loan_copy_parser = subparsers.add_parser('loan_copy', help="Abre un loan para la copia especificada al usuario especificado por la cantidad de dias especificados.")
    loan_copy_parser.add_argument('id', type=int, help="ID de la copy a prestar.")
    loan_copy_parser.add_argument('username', help="Username del usuario que hace el prestamo.")
    loan_copy_parser.add_argument('days', type=valid_days, help="Cantidad de dias que dura el prestamo.")
    
    return_copy_parser = subparsers.add_parser('return_copy', help="Cierra un prestamo activo.")
    return_copy_parser.add_argument('copy', type=int, help="ID de la copy que sera devuelta.")

    list_loans_parser = subparsers.add_parser('list_loans', help="Muestra los laons segun los filtros aplicados.")
    list_loans_parser.add_argument('-a', '--active', action='store_true', help="Muestra los loans activos.")
    list_loans_parser.add_argument('-t', '--historical', action='store_true', help="Muestra los prestamos ianctivos (historicos)")
    
    return parser.parse_args()