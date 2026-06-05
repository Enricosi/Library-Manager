import argparse

def parse_args():
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
    add_copy_parser.add_argument('book', help="ID del libro al que se le quiere crear una copia.")
    add_copy_parser.add_argument('-l', '--location', help="Indica la shelf location de la copia en la tienda.")

    remove_coy_parser = subparsers.add_parser('remove_copy', help="Elimina una copia de un libro debe tener un status distinto a loan.")
    remove_coy_parser.add_argument('id', help="ID de la copia que se va a eliminar.")

    change_copy_status_parser = subparsers.add_parser('change_copy_status', help="Cambia el status de una copy pero no puede cambiarlo a loaned.")
    change_copy_status_parser.add_argument('copy', help="ID de la copy a modificar")
    change_copy_status_parser.add_argument('new_status', choices=['damaged', 'lost', 'available'], help="Posibles ststus que puede tener una copy si se cambia desde este comando.Reglas: available → damaged, lost | loaned  → damaged, lost  (cierra el loan automáticamente) | damaged → available, lost | lost → available |")
    
    list_copies_parser = subparsers.add_parser('list_copies', help="Muestra las copias existentes segun los filtros aplicados")
    list_copies_parser.add_argument('-t', '--title', help="Filtra las copias por titulo.")
    list_copies_parser.add_argument('-s', '--status', choices=['avilable', 'loaned', 'damaged', 'lost'], help="Filtra las copias por estado.")
    
    add_user_parser = subparsers.add_parser('add_user', help="Agrega un nuevo usuario a la base de datos.")
    add_user_parser.add_argument('username', help="Username del user.")
    add_user_parser.add_argument('first_name', help="Primer nombre del user.")
    add_user_parser.add_argument('last_name', help="Apellido del user.")

    remove_user_parser = subparsers.add_parser('remove_user', help="Elimina un usuario de la base de datos si no tiene ningun loan activo.")
    remove_user_parser.add_argument('username', help="Username del user que se quiere eliminar.")


    return parser.parse_args()