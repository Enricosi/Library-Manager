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
    
    list_book_parser = subparsers.add_parser('list_books', help="Muestra todos los libros segun los filtros aplicados.")
    list_book_parser.add_argument('-t', '--title', help="Muesta si existe el libro con ese titulo.")
    list_book_parser.add_argument('-g', '--genre', help="Muestra los libros del genero especificado.")
    list_book_parser.add_argument('-a', '--author', help="Muestra los libros del autor especificado")

    add_copy_parser = subparsers.add_parser('add_copy', help="Agrega una copia fisica de un libro existente en la base de datos.")
    add_copy_parser.add_argument('book', help="ID del libro al que se le quiere crear una copia.")
    add_copy_parser.add_argument('-l', '--location', help="Indica la shelf location de la copia en la tienda.")


    return parser.parse_args()