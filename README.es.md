# Library Manager CLI

[English](README.md) · **Español**

CLI para gestionar libros, copias físicas, usuarios y préstamos de una biblioteca, con persistencia en MySQL.

## Requisitos

- Python 3.8+
- MySQL 8.0.13+

## Configuración

```bash
pip install -r requirements.txt

mysql -u <usuario> -p -e "CREATE DATABASE library_manager"
mysql -u <usuario> -p library_manager < schema.sql

cp .env.example .env   # luego completa tus valores
```

```env
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=library_manager
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Uso

```bash
python library_manager.py <comando> [argumentos]
```

---

## Comandos

### Libros

#### `add_book`
Agrega un libro.

| Argumento | Descripción |
|-----------|-------------|
| `title` | Título del libro |
| `author` | Autor del libro |
| `genre` | Género del libro |
| `-y`, `--year` | Año de publicación (opcional) |
| `-n`, `--isbn` | ISBN (opcional, único) |

```bash
python library_manager.py add_book "1984" "George Orwell" "Distopia" -y 1949 -n 9780451524935
```

#### `remove_book`
Elimina un libro por ID. Solo si no tiene copias asociadas.

```bash
python library_manager.py remove_book <id>
```

#### `list_book`
Lista libros, opcionalmente filtrados.

| Opción | Descripción |
|--------|-------------|
| `-t`, `--title` | Filtra por título (coincidencia parcial) |
| `-g`, `--genre` | Filtra por género (coincidencia parcial) |
| `-a`, `--author` | Filtra por autor (coincidencia parcial) |

```bash
python library_manager.py list_book -g Distopia
```

---

### Copias

#### `add_copy`
Agrega una copia física de un libro existente.

| Argumento | Descripción |
|-----------|-------------|
| `book` | ID del libro |
| `-l`, `--location` | Ubicación en estantería (opcional) |

```bash
python library_manager.py add_copy 1 -l "Estante A3"
```

#### `remove_copy`
Elimina una copia por ID. Solo si su estado no es `loaned`.

```bash
python library_manager.py remove_copy <id>
```

#### `change_copy_status`
Cambia el estado de una copia. No permite cambiar a `loaned` directamente.

| Argumento | Descripción |
|-----------|-------------|
| `copy` | ID de la copia |
| `new_status` | Nuevo estado: `damaged`, `lost` o `available` |

Reglas de transición:
- `available` → `damaged`, `lost`
- `loaned` → `damaged`, `lost` (cierra el préstamo automáticamente)
- `damaged` → `available`, `lost`
- `lost` → `available`

```bash
python library_manager.py change_copy_status 5 damaged
```

#### `list_copies`
Lista copias con el título del libro asociado.

| Opción | Descripción |
|--------|-------------|
| `-t`, `--title` | Filtra por título del libro |
| `-s`, `--status` | Filtra por estado: `available`, `loaned`, `damaged`, `lost` |

```bash
python library_manager.py list_copies -s available
```

---

### Usuarios

#### `add_user`
Registra un nuevo usuario.

| Argumento | Descripción |
|-----------|-------------|
| `username` | Nombre de usuario (único) |
| `first_name` | Nombre |
| `last_name` | Apellido |

```bash
python library_manager.py add_user jdoe John Doe
```

#### `remove_user`
Elimina un usuario por username. Solo si no tiene préstamos activos.

```bash
python library_manager.py remove_user <username>
```

#### `change_user_activity`
Cambia el estado de actividad de un usuario (activo ↔ inactivo). No permite desactivar a un usuario con préstamos activos.

```bash
python library_manager.py change_user_activity <username>
```

#### `list_users`
Lista usuarios, opcionalmente filtrados.

| Opción | Descripción |
|--------|-------------|
| `-a`, `--active` | Solo usuarios activos |
| `-i`, `--inactive` | Solo usuarios inactivos |
| `-l`, `--have_loans` | Solo usuarios con préstamos activos (muestra la cantidad) |

`--active` e `--inactive` son mutuamente excluyentes.

```bash
python library_manager.py list_users --have_loans
```

---

### Préstamos

#### `loan_copy`
Presta una copia disponible a un usuario activo.

| Argumento | Descripción |
|-----------|-------------|
| `id` | ID de la copia |
| `username` | Username del usuario |
| `days` | Duración del préstamo en días (1-60) |

```bash
python library_manager.py loan_copy 5 jdoe 14
```

#### `return_copy`
Cierra el préstamo activo de una copia y la marca como `available`.

```bash
python library_manager.py return_copy <copy_id>
```

#### `list_loans`
Lista préstamos con el título del libro y el username del usuario.

| Opción | Descripción |
|--------|-------------|
| `-a`, `--active` | Solo préstamos activos (sin devolver) |
| `-t`, `--historical` | Solo préstamos ya devueltos |

`--active` y `--historical` son mutuamente excluyentes.

```bash
python library_manager.py list_loans --active
```
