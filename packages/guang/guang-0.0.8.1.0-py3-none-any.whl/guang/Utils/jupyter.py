from IPython.core.interactiveshell import InteractiveShell
# import imp
import importlib


def output(flag='all'):
    """
    'all', 'last', 'last_expr' or 'none'
    """
    InteractiveShell.ast_node_interactivity = flag


def reload(module):
    # imp.reload(module)
    importlib.reload(module)
