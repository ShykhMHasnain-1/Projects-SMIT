import csv

def Search_By_Category():
    print("*"*50)
    print("1.Food")
    print("2.Transport")
    print("3.Shopping")
    print("4.Utility Bills")
    print("5.Entertainment")
    print("6.Education")
    print("7.Medical")
    print("8.Travel")
    print("9.Other")
    print("*"*50)
    user_category = int(input("Enter Choice(1/2/3/4/5/6/7/8):"))
    print("*"*50)

    if user_category == 1:
       with open("Projects\Expense\Food_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total_Food_Expense += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In Food is Rs.{Total_Food_Expense}")

    elif user_category == 2:
       with open("Projects\Expense\Transport_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total_Transport_Expense += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In Transport is Rs.{Total_Transport_Expense}")

        
    if user_category == 3:
       with open("Projects\Expense\Shopping_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total_Shopping_Expense += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In Shopping is Rs.{Total_Shopping_Expense}")
    
    if user_category == 4:
       with open("Projects/Expense/Utilitybills_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total_Utility_Bills_Expense += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In Utility Bills is Rs.{Total_Utility_Bills_Expense}")
    
    if user_category == 5:
       with open("Projects\Expense\Entertainment_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total_Entertainment_Expense += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In Entertainment is Rs.{Total_Entertainment_Expense}")
    
    if user_category == 6:
       with open("Projects\Expense\Education_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total_Education_Expense += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In Education is Rs.{Total_Education_Expense}")

    if user_category == 7:
       with open("Projects\Expense\Medical_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total_Medical_Expense += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In Medical is Rs.{Total_Medical_Expense}")
    
    if user_category == 8:
       with open("Projects\Expense\Travel_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total_Travel_Expense += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In Travel is Rs.{Total_Travel_Expense}")
    
    if user_category == 9:
       expense_category = input("Please Enter The Expense Category Name That You Have Added In Add Expense"
       "(First Letter Must Be Capital):")
       with open(f"Projects\Expense\{expense_category}_Expense.csv","r") as file:
            expense = csv.reader(file)
            for rows in expense:
                Spending_Amount = rows[1]
                Spending_Date = rows[2]
                Total += Spending_Amount
                print(f"Date: {Spending_Date} || Amount:{Spending_Amount}")
            print(f"Total Spending In {user_category} is Rs.{Total}")
                      
def Categories():
        Expense_Date_Input = input("Enter The Date:")

        print("*"*50)
        print("1.Food")
        print("2.Transport")
        print("3.Shopping")
        print("4.Utility Bills")
        print("5.Entertainment")
        print("6.Education")
        print("7.Medical")
        print("8.Travel")
        print("9.Other")
        print("*"*50)
        user_category = int(input("Enter Choice(1/2/3/4/5/6/7/8):"))
        print("*"*50)
        if user_category == 1:
            Expense_Amount = int(input("Enter The Amount In Food Expense: "))
            print(f"Amount Of Rs.{Expense_Amount} Spend On Food On Date:{Expense_Date_Input}")
            with open("Projects\Expense\Food_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category:Food | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print("------- Expense Added In File : Food_Expense.csv -------")
                
        elif user_category == 2:
            Expense_Amount = int(input("Enter The Spending Amount In Transport Expense: "))
            print(f"Amount Of Rs.{Expense_Amount} Spend On Transport On Date:{Expense_Date_Input}")
            with open("Projects\Expense\Transport_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category:Transport | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print("------- Expense Added In File : Transport_Expense.csv -------") 

        elif user_category == 3:
            Expense_Amount = int(input("Enter The Spending Amount In Shopping Expense: "))
            print(f"Amount Of Rs.{Expense_Amount} Spend On Shopping On Date:{Expense_Date_Input}")
            with open("Projects\Expense\Shopping_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category:Shopping | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print("------- Expense Added In File : Shopping_Expense.csv -------")
        
        elif user_category == 4:
            Expense_Amount = int(input("Enter The Spending Amount In Utility Bills Expense: "))
            with open("Projects\\Expense\\Utility_Bills_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category: Utility Bills | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print(f"Amount Of Rs.{Expense_Amount} Spend On Utility Bills On Date:{Expense_Date_Input}")
            print("------- Expense Added In File : Utility_Bills_Expense.csv -------")

        elif user_category == 5:
            Expense_Amount = int(input("Enter The Spending Amount In Entertainment Expense: "))
            with open("Projects\Expense\Entertainment_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category: Entertainment | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print(f"Amount Of Rs.{Expense_Amount} Spend On Entertainment On Date:{Expense_Date_Input}")
            print("------- Expense Added In File : Entertainment_Expense.csv -------")

        elif user_category == 6:
            Expense_Amount = int(input("Enter The Spending Amount In Education Expense: "))
            print(f"Amount Of Rs.{Expense_Amount} Spend On Education On Date:{Expense_Date_Input}")
            with open("Projects\Expense\Education_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category: Education | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print("------- Expense Added In File : Edication_Expense.csv -------")

        elif user_category == 7:
            Expense_Amount = int(input("Enter The Spending Amount In Medical Expense: "))
            print(f"Amount Of Rs.{Expense_Amount} Spend On Medical On Date:{Expense_Date_Input}")
            with open("\Projects\Expense\Medical_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category: Medical | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print("------- Expense Added In File : Medical_Expense.csv -------")

        elif user_category == 8:
            Expense_Amount = int(input("Enter The Spending Amount In Travel Expense: "))
            print(f"Amount Of Rs.{Expense_Amount} Spend On Travel On Date:{Expense_Date_Input}")
            with open("Projects\Expense\Travel_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category: Travel | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print("------- Expense Added In File : Travel_Expense.csv -------")
        elif user_category == 9:
            print()
            expense_category = input("Please Enter The Expense Category Name:")
            Expense_Amount = int(input(f"Enter The Spending Amount In {expense_category} Expense: "))
            print(f"Amount Of Rs.{Expense_Amount} Spend On {expense_category} On Date:{Expense_Date_Input}")
            with open(f"Projects\Expense\{expense_category}_Expense.csv","w") as file:
                expense = csv.writer(file)
                expense.writerow([f"Category: {expense_category} | Spending_Amount:{Expense_Amount} | Date:{Expense_Date_Input}"])
            print(f"------- Expense Added In File : {expense_category}_Expense.csv -------")
        else:
            print("Invalid Options!!!...")
    
def Add_Expense():
    Categories()   
    Menu()
def View_Expense():
    pass
def Total_Expense():
    with open(f"Projects\Expense\_Expense.csv","r") as folder:
        Total_Expense = csv.reader(folder)
        for rows in Total_Expense:
            total_expense += rows[1]
        print("The Total Expense : Rs.",total_expense)
def Menu():
    while True:
        print("="*50)
        print(" "*10,"Personal Expense Tracker")
        print("="*50)
        print(" "*20,"Menu")
        print("="*50)
        print("1.Add Expense\n2.View Expense\n3.Total Expense\n4.Search By Category\n5.Exit")
        print("="*50)
        try:
            user_choice = int(input("Enter Choice (1/2/3/4/5):"))
            print("="*50)
        except ValueError:
            print("Enter Number Only!!")
            continue
        if user_choice == 1:
            Add_Expense()
        elif user_choice == 2:
            View_Expense()
        elif user_choice == 3:
            Total_Expense()
        elif user_choice == 4:
            Search_By_Category()
        elif user_choice == 5:
            break
Menu()