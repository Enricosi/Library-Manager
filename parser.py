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
    remove_book_parser.add_argument('id', type=int, help="Titulo del libro que sera eliminado.")
    
    list_book_parser = subparsers.add_parser('list_books', help="Muestra todos los libros segun los filtros aplicados.")
    list_book_parser.add_argument('-t', '--title', help="Muesta si existe el libro con ese titulo.")
    list_book_parser.add_argument('-g', '--genre', help="Muestra los libros del genero especificado.")
    list_book_parser.add_argument('-a', '--author', help="Muestra los libros del autor especificado")

    return parser.parse_args()