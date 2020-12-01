import msvcrt # windows only


class console_view():
    def __init__(self, model,controller):
        self.__is_running = True;
        self.__model = model
        self.__controller = controller

    def quit(self):
        return None

    def print_message(self,message,callback = None):
        print(message)
        if callback is not None:
            return callback
        return None

    def print_table(self,table,callback = None):
        print(table[0])
        for row in table[1]:
            print(row)
        if callback is not None:
            return callback
        return None

    def get_input(self,callback = None):
        inp = input()
        if callback is not None:
            pass

    def main_menu(self):
        print('Select:')
        print('1)Show')
        print('2)Insert')
        print('3)Delete')
        print('4)Change')
        print('5)Generate')
        print('6)Querry')
        print('7)Quit')
        char = chr(msvcrt.getch()[0])
        return self.__controller.main_menu(char)

    def show_menu(self):
        table_names = self.__model.get_table_names()
        print('SHOW MENU')
        print('Choose table or write :r to return')
        print(table_names)
        answer = input()
        return self.__controller.show_menu(answer)
    
    def choose_delete_menu(self):
        table_names = self.__model.get_table_names()
        print('DELETE MENU')
        print('Choose table or write :r to return')
        print(table_names)
        answer = input()
        return self.__controller.choose_delete_menu(answer)

    def choose_insert_menu(self):
        table_names = self.__model.get_table_names()
        print('INSERT MENU')
        print('choose table or write :r to return')
        print(table_names)
        answer = input()
        return self.__controller.choose_insert_menu(answer)

    def choose_change_menu(self):
        table_names = self.__model.get_table_names()
        print('CHANGE MENU')
        print('Choose table or write :r to return')
        print(table_names)
        answer = input()
        return self.__controller.choose_change_menu(answer)

    def choose_generate_menu(self):
        table_names = self.__model.get_table_names()
        print('GENERATE MENU')
        print('Choose table or write :r to return')
        print(table_names)
        answer = input()
        return self.__controller.choose_generate_menu(answer)
    
    def choose_query_menu(self,query_list):
        print("Choose query")
        for i in range(0,len(query_list)):
            print(i+1,":",query_list[i])
        answer = input()

        return self.__controller.choose_query_menu(answer)
    
    def insert_row_menu(self,table_name,columns_data):
        print('Input data',table_name)
        answer = {}
        
        for data in columns_data:
            print(data[0],'(',data[1],'):',end=' ')
            inp = input()
            answer.update({data[0] : inp})

        return self.__controller.insert_data(table_name,answer)
    
    def change_row_menu(self,table_name,columns_data):
        print('Input data',table_name)
        answer = {}
        
        for data in columns_data:
            print(data[0],'(',data[1],'):',end=' ')
            inp = input()
            answer.update({data[0] : inp})
        print('WHERE',end =' ')
        inp = input()
        answer.update({'condition' : inp})

        return self.__controller.change_data(table_name,answer)

    def delete_row_menu(self,table_name,column_arr):
        print(table_name)
        print("Columns")
        print(column_arr)
        #self.__model.get
        print("WHERE",end = " ")
        answer = input()
        return self.__controller.delete_data(table_name,answer)

    def generate_size_menu(self,table_name):
        print('Input N:')
        answer = input()
        return self.__controller.generate_data(table_name,answer)

    def cond_query_menu(self,query_num):
        print("QUERY")
        print("WHERE",end = " ")
        cond = input()
        return self.__controller.cond_query_menu(query_num,cond)


