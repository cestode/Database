import psycopg2
from console_view import console_view
from db_model import db_model
from controller import controller
import os

def main():
    model = db_model('l2','postgres','1','127.0.0.1')
    cont = controller(model)
    view = console_view(model,cont)
    cont.set_view(view)
    func = view.main_menu()
    while func is not None:
        func = func()

if __name__ == '__main__':
    main()