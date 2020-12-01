class controller():
    def __init__(self, model):
        self.__model = model
        self.__query_data = ["article + theme","users + passport","comment + user + article", "read + user + article"]

    def set_view(self,view):
        self.__view = view

    def get_view_func(self,name,*args):
        return lambda : getattr(self.__view, name)(*args)

    def check_input(self,data,prev_menu = "main_menu"):

        if data == ':menu':
            return self.get_view_func("main_menu")

        if data == ':r':
            return self.get_view_func(prev_menu)

        if data == ':q':
            return self.get_view_func("quit")

    def main_menu(self,answer):
        if answer == '1':
            return self.get_view_func("show_menu")
        if answer == '2':
            return self.get_view_func("choose_insert_menu")
        if answer == '3':
            return self.get_view_func("choose_delete_menu")
        if answer == '4':
            return self.get_view_func("choose_change_menu")
        if answer == '5':
            return self.get_view_func("choose_generate_menu")
        if answer == '6':
            return self.get_view_func("choose_query_menu",self.__query_data)
        if answer == '7':
            return self.get_view_func("quit")

        return self.get_view_func("main_menu")

    def show_menu(self,data):
        
        res = self.check_input(data)
        if res is not None:
            return res

        model_data = self.__model.get_data(data)

        if type(model_data) == str:
            return self.get_view_func("print_message",model_data,self.get_view_func("show_menu"))

        return self.get_view_func("print_table",model_data,self.get_view_func("show_menu"))

    def check_table(self,table_name,curr_menu):

        if table_name not in self.__model.get_table_names():
            return self.get_view_func("print_message","unknown table {0}".format(table_name),self.get_view_func(curr_menu))
        
        return None


    def choose_insert_menu(self,data):

        res = self.check_input(data)
        if res is not None:
            return res
        
        res = self.check_table(data,"choose_insert_menu")
        
        if res is not None:
            return res

        return self.get_view_func("insert_row_menu",data,self.__model.get_column_types(data)[1:])

    def choose_delete_menu(self,data):

        res = self.check_input(data)
        if res is not None:
            return res

        res = self.check_table(data,"choose_delete_menu")
        
        if res is not None:
            return res

        column_arr = [x[0] for x in self.__model.get_column_types(data)]

        return self.get_view_func("delete_row_menu",data,column_arr)

    def choose_change_menu(self,data):

        res = self.check_input(data)
        if res is not None:
            return res

        res = self.check_table(data,"choose_change_menu")
        
        if res is not None:
            return res

        return self.get_view_func("change_row_menu",data,self.__model.get_column_types(data)[1:])

    def choose_generate_menu(self,data):
        res = self.check_input(data)
        if res is not None:
            return res

        res = self.check_table(data,"choose_generate_menu")
        
        if res is not None:
            return res

        return self.get_view_func("generate_size_menu",data)

    def choose_query_menu(self,data):
        res = self.check_input(data)
        if res is not None:
            return res

        int_data = 0
        res_func = None
        try:
            int_data = int(data)
            res_func = self.get_view_func("cond_query_menu",int_data)
        except Exception as e:
            res_func = self.get_view_func("print_message",str(e),self.get_view_func("choose_query_menu",self.__query_data))

        return res_func



    def change_data(self,table :str ,new_data : dict):

        res = self.check_input(new_data,"choose_change_menu")
        if res is not None:
            return res

        message = " "
        
        try:
            self.__model.change_data(table,new_data)
            message = "Success"
        except Exception as e:
            message = str(e) 
            self.__model.clear_transaction()

        column_data = self.__model.get_column_types(table)
        return self.get_view_func("print_message",message,self.get_view_func("choose_change_menu")) 

    def insert_data(self,table :str ,data : dict):
        
        res = self.check_input(data,"choose_insert_menu")
        if res is not None:
            return res

        message = " "
        try:
            self.__model.insert_data(table,data)
            message = "Success"
        except Exception as e:
            message = str(e) 
            self.__model.clear_transaction()

        return self.get_view_func("print_message",message,self.get_view_func("choose_insert_menu")) 
        

    def delete_data(self,table :str ,data : str):
        res = self.check_input(data,"choose_delete_menu")
        message = " "
        if res is not None:
            return res
        try:
            self.__model.delete_data(table,data)
            message = "Success"
        except Exception as e:
            message = str(e) 
            self.__model.clear_transaction()

        column_arr = [x[0] for x in self.__model.get_column_types(table)]

        return self.get_view_func("print_message",message,self.get_view_func("delete_row_menu",table,column_arr)) 

    def generate_data(self,table_name,data):
        res = self.check_input(data,"choose_generate_menu")
        
        if res is not None:
            return res

        message = " "
        data_int = 0

        try:
            data_int = int(data)
        except Exception as e:
            return self.get_view_func("print_message",str(e),self.get_view_func("generate_size_menu",table_name)) 

        
        if res is not None:
            return res

        if table_name == 'users':
            try:
                self.__model.generate_data_for_users(data_int)
                message = "Success"
            except Exception as e:
                message = str(e) 
                self.__model.clear_transaction()
        else:
            try:
                self.__model.generate_data(table_name,data_int)
                message = "Success"
            except Exception as e:
                message = str(e) 
                self.__model.clear_transaction()

        return self.get_view_func("print_message",message,self.get_view_func("generate_size_menu",table_name))

    def cond_query_menu(self,query_num,cond):

        if cond == ':menu':
            return self.get_view_func("main_menu")

        if cond == ':r':
            return self.get_view_func("choose_query_menu",self.__query_data)

        if cond == ':q':
            return self.get_view_func("quit")

        query_func = None
        if query_num == 1:
            query_func = getattr(self.__model, "join_article_theme")
        elif query_num == 2:
            query_func = getattr(self.__model, "join_users_passport")
        elif query_num == 3:
            query_func = getattr(self.__model, "join_comment_user_article")
        elif query_num == 4:
            query_func = getattr(self.__model, "join_readby_user_article")

        ret_func = None
        try:
            data = query_func(cond)
            ret_func = self.get_view_func("print_table",("execution time {} ms".format(data[0]),data[1]),self.get_view_func("cond_query_menu",query_num))
        except Exception as e:
            ret_func = self.get_view_func("print_message",str(e),self.get_view_func("cond_query_menu",query_num))
            self.__model.clear_transaction()

        return ret_func

        





