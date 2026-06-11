from commands_book import *
from commands_copy import *
from commands_users import *

def dispatch(args, conn):
    """Route parsed CLI arguments to the corresponding command handler.

    Looks up args.command in a dispatch table and calls the matching function,
    passing the full args namespace so each handler can read its own arguments.

    Args:
        args (argparse.Namespace): Parsed arguments returned by parse_args(),
            must include a 'command' attribute.

    Returns:
        Any: Whatever the invoked command handler returns.

    Raises:
        RuntimeError: If args.command does not match any known command.
    """
    handlers = {
        'add_book':cmd_add_book,
        'remove_book':cmd_remove_book,
        'list_book':cmd_list_book,
        'add_copy':cmd_add_copy,
        'remove_copy':cmd_remove_copy,
        'change_copy_status':cmd_change_copy_status,
        'list_copies':cmd_list_copies,
        'add_user':cmd_add_user,
        'remove_user':cmd_remove_user,
        'cahange_user_activity':cmd_change_user_activity,
        'list_users':cmd_list_users,
    }

    cmd = args.command

    fn  = handlers.get(cmd)

    if fn is None:
        raise RuntimeError('Comando desconocido')
    
    return fn(args, conn)