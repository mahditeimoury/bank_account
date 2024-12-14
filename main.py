import mahdi
from mahdi import connection as CO
from prettytable import PrettyTable
from tkinter import messagebox
from customtkinter import *
from manager import Manager
from clerck import Clerck
from customer import Customer

manager_list = []
global window4
clerck_list = []


def load_data3():
    clerck_list = []
    term1=0
    query = """
                    select *
                    from clerk
                    where is_deleted=?
                    """
    data= term1
    data2 = mahdi.connection2(query, data)
    for item in data2:
        clerck_item = Clerck(item[0], item[1], item[2], item[3], item[4], item[6], item[7])
        clerck_list.append(clerck_item)

    return clerck_list


def load_data2():
    manager_list = []
    query = """select * from manager"""
    data1 = CO(query)
    for item in data1:
        manager_item = Manager(item[0], item[1], item[2])
        manager_list.append(manager_item)

    return manager_list


def main(id_clerk=None):
    def load_data(term=None):
        customer_list = []
        if term:
            term1 = search_entry.get()
            query = f"""select *
                        from customer
                        where first_name like '%{term1}%' or last_name like '%{term1}%'
                        or national_code like '%{term1}%'
            """
            data3 = CO(query)

        else:
            term1 = 0
            query = f"""
                                    select *
                                    from customer
                                    where is_deleted=?
                                    """
            data3 = mahdi.connection2(query, term1)
        for item in data3:
            customer_item = Customer(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[9], item[12])
            customer_list.append(customer_item)

        return customer_list

    window2 = CTk()
    window2.title("Clerk Account")

    search_entry = CTkEntry(window2, width=100, corner_radius=15, text_color="violet")
    search_entry.grid(row=0, column=1, pady=10, padx=10)

    row_label=CTkLabel(window2, text="Row")
    row_label.grid(row=1, column=0, pady=10, padx=10)

    first_name_label = CTkLabel(window2, text="First Name")
    first_name_label.grid(row=1, column=1, padx=10, pady=10)

    last_name_label = CTkLabel(window2, text="Last Name")
    last_name_label.grid(row=1, column=2, padx=10, pady=10)

    national_code_label = CTkLabel(window2, text="National Code")
    national_code_label.grid(row=1, column=3, padx=10, pady=10)

    table_body_list = []

    def create_table_body():
        for item in table_body_list:
            item.destroy()
        table_body_list.clear()
        if search_entry.get():
            customer_list = load_data(search_entry.get())
        else:
            customer_list = load_data()
        row_number = 1
        for customer in customer_list:
            row_entry = CTkEntry(window2, width=10)
            row_entry.grid(row=row_number + 1, column=0, pady=10)
            row_entry.insert(0, row_number)
            row_entry.configure(state="readonly")
            table_body_list.append(row_entry)

            first_name_entry = CTkEntry(window2, width=100, corner_radius=15)
            first_name_entry.grid(row=row_number + 1, column=1, pady=10, padx=10)
            first_name_entry.insert(0, customer.first_name)
            first_name_entry.configure(state="readonly")
            table_body_list.append(first_name_entry)

            last_name_entry = CTkEntry(window2, width=100, corner_radius=15)
            last_name_entry.grid(row=row_number + 1, column=2, pady=10, padx=10)
            last_name_entry.insert(0, customer.last_name)
            last_name_entry.configure(state="readonly")
            table_body_list.append(last_name_entry)

            national_code_entry = CTkEntry(window2, width=100, corner_radius=15)
            national_code_entry.grid(row=row_number + 1, column=3, pady=10, padx=10)
            national_code_entry.insert(0, customer.national_code)
            national_code_entry.configure(state="readonly")
            table_body_list.append(national_code_entry)

            def operation(id, first, last, mothername, national_c, phone, address, status, account):
                fullname = f"{first} {last}"
                account_number = account.split("-")[4]
                window4 = CTk()
                window4.title("Operation")
                fullname_lbl = CTkLabel(window4, text="Full Name", corner_radius=20)
                fullname_lbl.grid(row=0, column=0, padx=10, pady=10)
                fullname_entry = CTkEntry(window4, width=100)
                fullname_entry.grid(row=0, column=1, pady=10)
                fullname_entry.insert(0, fullname)
                fullname_entry.configure(state="readonly")

                mothername_lbl = CTkLabel(window4, text="Mother Name", corner_radius=20)
                mothername_lbl.grid(row=0, column=2, padx=(20, 0), pady=10)
                mothername_entry = CTkEntry(window4, width=100)
                mothername_entry.grid(row=0, column=3, pady=10)
                mothername_entry.insert(0, mothername)
                mothername_entry.configure(state="readonly")

                def block(id3):
                    if status:
                        term5 = 0
                        block_button.configure(text="Unblock", fg_color="red")
                        block_button.grid(row=0, column=4, padx=(20, 0), pady=10)
                    else:
                        term5 = 1
                        block_button.configure(text="Block", fg_color="blue")
                        block_button.grid(row=0, column=4, padx=(20, 0), pady=10)
                    query = """
                           UPDATE customer
                            set is_active = ?
                            where id = ?
                            """
                    dat = (term5, id3)
                    mahdi.iud(query, dat)
                    create_table_body()

                block_button = CTkButton(window4, text="Block Account", corner_radius=20,
                                         command=lambda id3=id: block(id3))

                if status:
                    block_button.configure(text="Block", fg_color="blue")
                else:
                    block_button.configure(text="Unblock", fg_color="red")
                block_button.grid(row=0, column=4, padx=(20, 0), pady=10)

                def delete():
                    query1 = f"""
                    update customer
                    set is_deleted=?
                    where id=?
                    """
                    dat = (1, id)
                    mahdi.iud(query1, dat)
                    window4.destroy()
                    create_table_body()
                    messagebox.showinfo("DELETE", "Account Has Been Deleted")

                delete_button = CTkButton(window4, text="Delete", fg_color="blue", corner_radius=20,
                                          command=delete)
                delete_button.grid(row=0, column=5, padx=10, pady=10)

                national_lbl = CTkLabel(window4, text="National Code", corner_radius=20)
                national_lbl.grid(row=1, column=0, padx=(20, 0), pady=10)
                national_entry = CTkEntry(window4, width=100)
                national_entry.grid(row=1, column=1, pady=10)
                national_entry.insert(0, national_c)
                national_entry.configure(state="readonly")

                phone_lbl = CTkLabel(window4, text="Phone Number", corner_radius=20)
                phone_lbl.grid(row=1, column=2, padx=(20, 0), pady=10)
                phone_entry = CTkEntry(window4, width=100)
                phone_entry.grid(row=1, column=3, pady=10)
                phone_entry.insert(0, phone)
                phone_entry.configure(state="readonly")

                update_button = CTkButton(window4, text="Update Account", fg_color="blue", corner_radius=20,
                                          command=lambda id=id: new_account(id))
                update_button.grid(row=1, column=4, padx=(20, 0), pady=10)

                def deposit(id, term):
                    if status:
                        window5 = CTk()
                        if term:
                            window5.title("Withdraw")
                        else:
                            window5.title("Deposit")
                        window5.geometry("500x200")
                        amount_label = CTkLabel(window5, text="Amount")
                        amount_label.grid(row=1, column=0, pady=10, padx=(10, 0))
                        amount_entry = CTkEntry(window5, width=200, corner_radius=20)
                        amount_entry.grid(row=1, column=1, pady=10, padx=(0, 10))
                        way_label = CTkLabel(window5, text="Deposit Way")
                        way_label.grid(row=2, column=0, pady=10, padx=(10, 0))
                        values = ("Cash", "Cheque")

                        def choose(choice=None):
                            choice = way_combo.get()
                            serial_entry = CTkEntry(window5, width=200, placeholder_text="Serial Number")
                            if choice == "Cheque":
                                serial_entry.grid(row=2, column=2, pady=10, padx=(0, 20))
                                serial_entry.configure(state="normal")
                            elif choice == "Cash":
                                serial_entry.grid(row=2, column=2, pady=10, padx=(0, 20))
                                serial_entry.configure(state="readonly")

                        way_combo = CTkComboBox(window5, 100, values=values, command=choose)
                        way_combo.grid(row=2, column=1, pady=10)

                        def account_deposit():
                            phone1 = phone
                            answer = messagebox.askokcancel("Operation", "Are You Sure")
                            if answer:
                                if term:
                                    if int(amount_entry.get()) < int(balance_entry.get()):
                                        query = """
                                                           insert into history
                                                           (withdraw, customer_id)
                                                           values (?, ?)
                                                           """
                                        dat1 = (amount_entry.get(), id)
                                        mahdi.iud(query, dat1)
                                        text = f"مشتری گرامی مبلغ {amount_entry.get()} از حساب {account_number} برداشت گردید. مانده حساب شما مبلغ {int(balance_entry.get()) - int(amount_entry.get())} مبباشد. بانک مهدی امین مردم ایران زمین."
                                        customer.sms1(phone1, text)

                                    else:
                                        messagebox.showinfo("Crashed", "The Amount Of Withdraw Is More Than Account "
                                                                       "Balance")
                                else:
                                    query = """
                                        insert into history
                                        (deposite, customer_id)
                                        values (?, ?)
                                        """
                                    dat2 = (amount_entry.get(), id)
                                    mahdi.iud(query, dat2)

                                    text = f"مشتری گرامی مبلغ {amount_entry.get()} به حساب {account_number} واریز گردید. مانده حساب شما مبلغ {int(balance_entry.get()) + int(amount_entry.get())} می باشد. بانک مهدی امین مردم ایران زمین."
                                    customer.sms1(phone1, text)
                            window5.destroy()
                            window4.destroy()
                            operation(id, first, last, mothername, national_c, phone, address, status, account)

                        if term:
                            title_button = CTkButton(window5, text="Submit withdraw Operation",
                                                     command=account_deposit)
                        else:
                            title_button = CTkButton(window5, text="Submit Deposit Operation",
                                                     command=account_deposit)
                        title_button.grid(row=0, column=1, columnspan=2, pady=(0, 30))
                        window5.mainloop()
                    else:
                        messagebox.showinfo("Crashed",
                                            "The Operation Crashed Because The Account Is Blocked By Operator")

                deposit_button = CTkButton(window4, text="Deposit", corner_radius=20, fg_color="blue",
                                           command=lambda id=id, term=False: deposit(id, term))
                deposit_button.grid(row=1, column=5, padx=10, pady=10)

                address_lbl = CTkLabel(window4, text="Address", corner_radius=20)
                address_lbl.grid(row=2, column=0, padx=(20, 0), pady=10)
                address_entry = CTkTextbox(window4, width=120, height=120)
                address_entry.grid(row=2, column=1, pady=10, rowspan=2)
                address_entry.insert("0.0", address)
                address_entry.configure(state="disabled")

                balance_lbl = CTkLabel(window4, text="Balance", corner_radius=20)
                balance_lbl.grid(row=2, column=2, padx=(20, 0), pady=10)
                balance_entry = CTkEntry(window4, width=100)
                balance_entry.grid(row=2, column=3, pady=10)
                account_label = CTkLabel(window4, text="Account_number", corner_radius=20)
                account_label.grid(row=3, column=2, padx=(20, 0), pady=10)
                account_entry = CTkEntry(window4, width=120)
                account_entry.grid(row=3, column=3, pady=10)
                account_entry.insert(0, account_number)
                account_entry.configure(state="disabled")
                query = """
                                    SELECT sum(deposite-withdraw)
                                    from history
                                    group by customer_id
                                    having customer_id=?
                                    """
                data = mahdi.connection2(query, id)
                for item2 in data:
                    for term1 in item2:
                        term = int(term1)
                        query = f"""
                                       UPDATE customer
                                       set balance= ?
                                       where id = ?
                                       """
                        dat = (term, id)
                        mahdi.iud(query, dat)
                        balance_entry.insert(0, term)
                        balance_entry.configure(state="readonly")
                        query = f"""
                                        UPDATE history
                                        set balance=?
                                        where entry_date in (select max(entry_date) from history)
                                        """
                        dat = term
                        mahdi.iud(query, dat)

                withdraw_button = CTkButton(window4, text="Withdraw", corner_radius=20, fg_color="blue",
                                            command=lambda id=id, term=True: deposit(id, term))
                withdraw_button.grid(row=2, column=4, padx=(20, 0), pady=10)

                def report():
                    query3 = """
                            select first_name, last_name, national_code, deposite, withdraw, h.balance, h.entry_date
                            from customer cu
                            inner join history h on cu.id=h.customer_id
                            where cu.id=?
                    """
                    data_reports = mahdi.connection2(query3, id)
                    table = PrettyTable()
                    table.field_names = ["FirstName", "LastName", "NationalCode", "Deposit", "Withdraw", "Balance",
                                         "Date"]
                    for data5 in data_reports:
                        table.add_row(data5)
                    with open("test.txt", mode="w") as file:
                        file.write(str(table))
                    file.close()
                    messagebox.showinfo("Done", "The Report Is Ready")
                    window4.focus_force()

                report_button = CTkButton(window4, text="Report", corner_radius=20, fg_color="blue", command=report)
                report_button.grid(row=2, column=5, padx=20, pady=10)

                window4.mainloop()

            operation_button = CTkButton(window2, text="Operation", corner_radius=15,
                                         command=lambda id=customer.id, first=customer.first_name,
                                                        last=customer.last_name,
                                                        mothername=customer.mother_name,
                                                        national_c=customer.national_code, phone=customer.phone_number,
                                                        address=customer.address, status=customer.is_active, account=customer.account_no: operation(
                                             id, first, last, mothername,
                                             national_c, phone, address, status, account))
            operation_button.grid(row=row_number + 1, column=4, pady=10, padx=10)
            table_body_list.append(operation_button)
            row_number += 1

    create_table_body()

    def new_account(id=None):
        window3 = CTk()
        if id:
            window3.title("Update Account")
        else:
            window3.title("New Account")
        window3.geometry("700x300")
        window3.resizable(False, False)

        f_name_label = CTkLabel(window3, text="First Name", corner_radius=15)
        f_name_label.grid(row=1, column=0, padx=10, pady=10)
        f_name_entry = CTkEntry(window3, width=100, corner_radius=15)
        f_name_entry.grid(row=1, column=1, padx=10, pady=10)

        l_name_label = CTkLabel(window3, text="Last Name", corner_radius=15)
        l_name_label.grid(row=2, column=0, pady=10)
        l_name_entry = CTkEntry(window3, width=100, corner_radius=15)
        l_name_entry.grid(row=2, column=1, padx=10, pady=10)

        mother_name_label = CTkLabel(window3, text="Mother Name", corner_radius=15)
        mother_name_label.grid(row=3, column=0, pady=10)
        mother_name_entry = CTkEntry(window3, width=100, corner_radius=15)
        mother_name_entry.grid(row=3, column=1, padx=10, pady=10)

        nat_code_label = CTkLabel(window3, text="National Code", corner_radius=15)
        nat_code_label.grid(row=4, column=0, pady=10)
        nat_code_entry = CTkEntry(window3, width=100, corner_radius=15)
        nat_code_entry.grid(row=4, column=1, padx=10, pady=10)

        phone_label = CTkLabel(window3, text="Phone", corner_radius=15)
        phone_label.grid(row=1, column=2, pady=10)
        phone_entry = CTkEntry(window3, width=100, corner_radius=15)
        phone_entry.grid(row=1, column=3, padx=10, pady=10)

        address_label = CTkLabel(window3, text="Address", corner_radius=15)
        address_label.grid(row=2, column=2, pady=10)
        address_entry = CTkTextbox(window3, width=200, height=100, corner_radius=15)
        address_entry.grid(row=2, column=3, padx=10, pady=10)
        if id:
            query = """
            select first_name, last_name, mother_name, phone_number, national_code, address
            from customer
            where id =?
            """
            data = mahdi.connection2(query, id)
            for i in data:
                f_name_entry.insert(0, i[0])
                l_name_entry.insert(0, i[1])
                mother_name_entry.insert(0, i[2])
                phone_entry.insert(0, i[3])
                nat_code_entry.insert(0, i[4])
                address_entry.insert("1.0", i[5])

        def submit():

            if id:
                query = """
                UPDATE customer
                set first_name=?,
                last_name=?,
                mother_name=?,
                national_code=?,
                phone_number=?,
                address=?
                where id = ?
                """
                dat = (f_name_entry.get(), l_name_entry.get(), mother_name_entry.get(),
                       nat_code_entry.get(), phone_entry.get(), address_entry.get("1.0", "end"), id)
                mahdi.iud(query, dat)

            else:
                query = """
                        INSERT INTO customer (first_name, last_name, mother_name, national_code,
                        phone_number, address, balance, clerk_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """
                dat = (f_name_entry.get(), l_name_entry.get(), mother_name_entry.get(),
                       nat_code_entry.get(), phone_entry.get(), address_entry.get("1.0", "end"), 0, id_clerk)
                mahdi.iud(query, dat)

            create_table_body()
            window3.destroy()
            if id:
                messagebox.showinfo("Done", "Account Has Been Updated")
                # window4.destroy()
            else:
                messagebox.showinfo("Done", "New Account Has Been Created")

        if id:
            new_account_button = CTkButton(window3, text="Update Account Information", corner_radius=15
                                           , fg_color="#9900ff", command=submit)
        else:
            new_account_button = CTkButton(window3, text="Submit New Account Information", corner_radius=15
                                           , fg_color="#0099ff", command=submit)
        new_account_button.grid(row=0, column=2)

        window3.mainloop()

    new_account_button = CTkButton(window2, text="New Account", fg_color="#ff9933", command=new_account)
    new_account_button.grid(row=0, column=3)
    search_button = CTkButton(window2, text="Search", command=create_table_body)
    search_button.grid(row=0, column=0, padx=10, pady=10)

    window2.mainloop()


window = CTk()
window.title("Loging Page")
window.geometry("420x100")
window.resizable(False, False)
wind_label = CTkLabel(window, text="LOGGING PAGE")
wind_label.grid(row=0, column=1, pady=0, padx=0)

clerk_body_list = []


def manager_entry(manager_id=None):
    window7 = CTk()
    window7.title("Manager Operation")

    row_label = CTkLabel(window7, text="Row")
    row_label.grid(row=1, column=0, pady=10, padx=10)

    first_name_label = CTkLabel(window7, text="First Name")
    first_name_label.grid(row=1, column=1, padx=10, pady=10)

    last_name_label = CTkLabel(window7, text="Last Name")
    last_name_label.grid(row=1, column=2, padx=10, pady=10)

    def create_manager_body():

        row_number = 1
        clerck_list = load_data3()
        for item in clerk_body_list:
            item.destroy()
        clerk_body_list.clear()
        for clerk in clerck_list:
            row_entry = CTkEntry(window7, width=10)
            row_entry.grid(row=row_number + 1, column=0, pady=10)
            row_entry.insert(0, row_number)
            row_entry.configure(state="readonly")
            clerk_body_list.append(row_entry)

            first_name_entry = CTkEntry(window7, width=100, corner_radius=15)
            first_name_entry.grid(row=row_number + 1, column=1, pady=10, padx=10)
            first_name_entry.insert(0, clerk.first_name)
            first_name_entry.configure(state="readonly")
            clerk_body_list.append(first_name_entry)

            last_name_entry = CTkEntry(window7, width=100, corner_radius=15)
            last_name_entry.grid(row=row_number + 1, column=2, pady=10, padx=10)
            last_name_entry.insert(0, clerk.last_name)
            last_name_entry.configure(state="readonly")
            clerk_body_list.append(last_name_entry)

            def blocking(id1, status):
                if status:
                    term = 0
                else:
                    term = 1
                query="""
                                        UPDATE clerk
                                        set is_active = ?
                                        where id = ?
                                        """
                dat=(term, id1)
                mahdi.iud(query, dat)
                query = """
                            select count(id)
                            from clerk
                            where id <=?
                """
                data = mahdi.connection2(query, id1)
                for i in data:
                    for j in i:
                        data1 = int(j)
                        if status:
                            block_button.configure(text="Unblock", fg_color="red")
                            block_button.grid(row=data1 + 1, column=3, padx=10, pady=10)
                            create_manager_body()
                            messagebox.showinfo("Done", "Account Has Been Blocked")
                        else:
                            block_button.configure(text="Block", fg_color="blue")
                            block_button.grid(row=data1 + 1, column=3, padx=10, pady=10)
                            create_manager_body()
                            messagebox.showinfo("Done", "Account Has Been Unblocked")
                        clerk_body_list.append(block_button)

            if clerk.is_active:
                block_button = CTkButton(window7, text="Block", corner_radius=15,
                                         command=lambda id1=clerk.id, status=clerk.is_active: blocking(id1, status))
                block_button.grid(row=row_number + 1, column=3, pady=10, padx=10)
            else:
                block_button = CTkButton(window7, text="Unblock", corner_radius=15, fg_color="red",
                                         command=lambda id1=clerk.id, status=clerk.is_active: blocking(id1, status))
                block_button.grid(row=row_number + 1, column=3, pady=10, padx=10)
            clerk_body_list.append(block_button)

            def delete(id1):
                query = """
                update clerk
                set is_deleted = ?
                where id=?
                """
                dat = (1, id1)
                mahdi.iud(query, dat)
                create_manager_body()
                messagebox.showinfo("Done", "Account Has Been Deleted")

            delete_button = CTkButton(window7, text="Delete", corner_radius=15,
                                      command=lambda id1=clerk.id: delete(id1))
            delete_button.grid(row=row_number + 1, column=4, pady=10, padx=10)
            clerk_body_list.append(delete_button)

            update_button = CTkButton(window7, text="Update", corner_radius=15, command= lambda
                id2=clerk.id: new_clerk(id2))
            update_button.grid(row=row_number + 1, column=5, pady=10, padx=10)
            clerk_body_list.append(update_button)
            row_number += 1

    create_manager_body()

    def new_clerk(id=None):
        window8 = CTk()
        if id:
            window8.title("update Clerk")
        else:
            window8.title("New Clerk")
        f_name_label = CTkLabel(window8, text="First Name", corner_radius=15)
        f_name_label.grid(row=1, column=0, padx=10, pady=10)
        f_name_entry = CTkEntry(window8, width=100, corner_radius=15)
        f_name_entry.grid(row=1, column=1, padx=10, pady=10)

        l_name_label = CTkLabel(window8, text="Last Name", corner_radius=15)
        l_name_label.grid(row=2, column=0, pady=10)
        l_name_entry = CTkEntry(window8, width=100, corner_radius=15)
        l_name_entry.grid(row=2, column=1, padx=10, pady=10)

        user_name_label = CTkLabel(window8, text="User Name", corner_radius=15)
        user_name_label.grid(row=3, column=0, pady=10)
        user_name_entry = CTkEntry(window8, width=100, corner_radius=15)
        user_name_entry.grid(row=3, column=1, padx=10, pady=10)

        password_label = CTkLabel(window8, text="Password", corner_radius=15)
        password_label.grid(row=4, column=0, pady=10)
        password_entry = CTkEntry(window8, width=100, corner_radius=15)
        password_entry.grid(row=4, column=1, padx=10, pady=10)
        if id:
            query=f"""
                    select first_name, last_name, user_name, password, is_active
                    from clerk
                    where id=?
                    """
            data = mahdi.connection2(query, id)
            for i in data:
                f_name_entry.insert(0, i[0])
                l_name_entry.insert(0, i[1])
                user_name_entry.insert(0, i[2])
                password_entry.insert(0, i[3])

        def submit():
            if id:
                query=f"""
                        update clerk
                        set first_name = ?, last_name = ?, user_name = ?, password = ?"""
                dat = (f_name_entry.get(), l_name_entry.get(), user_name_entry.get(), password_entry.get())
            else:
                query = f"""
                      insert into clerk (first_name, last_name, user_name, password, manager_id)
                      values(? ,? ,?, ?, ?)
                """
                dat = (f_name_entry.get(), l_name_entry.get(), user_name_entry.get(), password_entry.get(), 1)
            mahdi.iud(query, dat)
            if id:
                messagebox.showinfo("Done", "Account Has Been Updated")
            else:
                messagebox.showinfo("Done", "New Clerk Has Been Created")
            window8.destroy()
            create_manager_body()

        if id:
            submit_button = CTkButton(window8, text="Update Clerk", corner_radius=15, command= submit)
        else:
            submit_button = CTkButton(window8, text="New Clerk Submit", corner_radius=15, command=submit)
        submit_button.grid(row=0, column=1, padx=(0, 70))
        window8.mainloop()

    new_clerk_button = CTkButton(window7, text="New Clerk", corner_radius=15, command=new_clerk)
    new_clerk_button.grid(row=0, column=3)
    window7.mainloop()


def clerk(term):
    window6 = CTk()
    window6.geometry("300x150")
    window6.grid_location(1000, 1000)
    window6.resizable(False, False)
    if term:
        window6.title("MANAGER LOGGING")
    else:
        window6.title("CLERK LOGGING")
    user_name_label = CTkLabel(window6, text="User Name")
    user_name_label.grid(row=1, column=0, pady=10, padx=10)
    user_name_entry = CTkEntry(window6, width=150, corner_radius=15)
    user_name_entry.grid(row=1, column=1, pady=10, padx=10)
    pass_label = CTkLabel(window6, text="Password")
    pass_label.grid(row=2, column=0, pady=10, padx=10)
    pass_entry = CTkEntry(window6, width=150, corner_radius=15)
    pass_entry.grid(row=2, column=1, pady=10, padx=10)

    def manager_login():
        manager_list = load_data2()
        for manager in manager_list:
            a = manager.user_name == user_name_entry.get()
            b = manager.password == pass_entry.get()
            c = a and b
            if c:
                manager_id = manager.id
                window6.destroy()
                window.destroy()
                manager_entry(manager_id)

                break
        if not c:
            messagebox.showinfo("Crashed", "User or Password is Wrong")
            window6.focus_force()

    def clerk_login():
        clerck_list = load_data3()

        for clerk in clerck_list:
            a = clerk.user_name == user_name_entry.get()
            b = clerk.password == pass_entry.get()
            c = clerk.is_active == 1
            d = a and b and c
            if d:
                id_clerk = clerk.id
                window6.destroy()
                window.destroy()
                main(id_clerk)
                break
        if not d:
            messagebox.showinfo("Crashed", "User or Password is Wrong or You Have Benn Blocked")
            window6.focus_force()

    if term:
        wind_button = CTkButton(window6, text="MANAGER LOGGING PAGE", command=manager_login)
    else:
        wind_button = CTkButton(window6, text="CLERK LOGGING PAGE", command=clerk_login)
    wind_button.grid(row=0, column=1)
    window6.mainloop()


clerk_button = CTkButton(window, text="کارمند", corner_radius=15, bg_color="blue",
                         command=lambda term=False: clerk(term))
clerk_button.grid(row=1, column=2, padx=10, pady=10)

managing_button = CTkButton(window, text="بانک مدیر", corner_radius=15, bg_color="red",
                            command=lambda term=True: clerk(term))
managing_button.grid(row=1, column=0, padx=10, pady=10)

window.mainloop()