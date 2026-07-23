Car_Stock = {}
Customer = {}
Sells = {}

while True:
    print("-" * 50)
    print(" " * 10, "Showroom Management System")
    print("-" * 50)
    print("1. Stock Management\n2. Customer Management\n3. Billing System\n4. Report\n5. Exit")
    print("-" * 50)
    user_input_choice = int(input("Enter The Choice(1/2/3/4/5): "))
    print("-" * 50)

    if user_input_choice == 1:
        while True:
            print("1. Add Stock\n2. View Stocks\n3. Update Stocks\n4. Delete Stocks\n5. Exit From S.M")
            user_input_choice_SM = int(input("Enter The Choice(1/2/3/4/5): "))
            print("-" * 50)

            if user_input_choice_SM == 1:
                Car_Name = input("Enter The Car Name: ")
                Car_Company = input("Enter The Car Company: ")
                Car_Model = int(input("Enter The Car Model (Year): "))
                Car_Price = int(input("Enter The Car Price: "))
                Car_Qty = int(input("Enter The Car Quantity: "))
                Car_Stock[Car_Name] = {
                    "Car Company": Car_Company,
                    "Model(Year)": Car_Model,
                    "Price": Car_Price,
                    "Quantity": Car_Qty
                }
                print("------- Stock Added Successfully...!!! -------")

            elif user_input_choice_SM == 2:
                for car_name, details in Car_Stock.items():
                    print("Car Name:          ||", car_name)
                    print("Manufact:Company : ||", details["Car Company"])
                    print("Car Model:         ||", details["Model(Year)"])
                    print("Price:             ||", details["Price"])
                    print("Quantity:          ||", details["Quantity"])
                    print("*" * 50)

            elif user_input_choice_SM == 3:
                Car_Name_To_Check = input("Enter The Car Name To Update: ")
                if Car_Name_To_Check in Car_Stock:
                    while True:
                        print("1. Update Car Name\n2. Update Car Company\n3. Update Car Model\n4. Update Car Price\n5. Update Car Quantity")
                        user_input_choice_update = int(input("Enter Your Choice:(1/2/3/4/5): "))
                        if user_input_choice_update == 1:
                            upd_car_name = input("Enter The Updated Car Name: ")
                            Car_Stock[upd_car_name] = Car_Stock.pop(Car_Name_To_Check)
                            print("------- Info Updated Successfully!!! -------")
                            Car_Name_To_Check = upd_car_name

                        elif user_input_choice_update == 2:
                            upd_car_comp = input("Enter The Updated Car Company: ")
                            Car_Stock[Car_Name_To_Check]["Car Company"] = upd_car_comp
                            print("------- Info Updated Successfully!!!")

                        elif user_input_choice_update == 3:
                            upd_car_model = int(input("Enter The Updated Car Model (Year): "))
                            Car_Stock[Car_Name_To_Check]["Model(Year)"] = upd_car_model
                            print("------- Info Updated Successfully!!!")

                        elif user_input_choice_update == 4:
                            upd_car_price = int(input("Enter The Updated Car Price: "))
                            Car_Stock[Car_Name_To_Check]["Price"] = upd_car_price
                            print("------- Info Updated Successfully!!!")

                        elif user_input_choice_update == 5:
                            upd_car_Qty = int(input("Enter The Updated Car Quantity: "))
                            Car_Stock[Car_Name_To_Check]["Quantity"] = upd_car_Qty
                            print("------- Info Updated Successfully!!!")

                        print("1. Want To Update Same Car\n2. Want To Update Another Car\n3. Exit From Update Mode")
                        choice = int(input("Enter Choice: "))
                        if choice == 1:
                            continue
                        elif choice == 2:
                            break
                        elif choice == 3:
                            break
                else:
                    print("Car not found in stock.")

            elif user_input_choice_SM == 4:
                Car_Name_To_Delete = input("Enter The Car Name To Delete: ")
                if Car_Name_To_Delete in Car_Stock:
                    del Car_Stock[Car_Name_To_Delete]
                    print(f"Item: {Car_Name_To_Delete} has been removed from stock.")
                else:
                    print("Car not found in stock.")

            elif user_input_choice_SM == 5:
                break

    elif user_input_choice == 2:
        C_Name = input("Enter The Customer Name: ")
        C_CNIC = input("Enter The Customer CNIC: ")
        C_Con_Numer = input("Enter The Customer Contact Number: ")
        C_Address = input("Enter The Customer Address: ")

        Customer[C_Name] = {
            "Customer CNIC": C_CNIC,
            "Customer Contact": C_Con_Numer,
            "Customer Address": C_Address
        }
        print("Customer added successfully.")

    elif user_input_choice == 3:
        Coustomer_Name = input("Enter Customer Name: ")
        if Coustomer_Name in Customer:
            Booked_Car_Name = input("Enter The Booked Car Name: ")
            if Booked_Car_Name in Car_Stock:
                if Car_Stock[Booked_Car_Name]["Quantity"] > 0:
                    Purchased_Date = input("Enter Booking Date: ")
                    Paid_Amount = int(input("Enter Paid Amount: "))
                    Booked_Car_Qty = int(input("Enter Booked Car Quantity: "))
                    if Car_Stock[Booked_Car_Name]["Quantity"] >= Booked_Car_Qty:
                        Car_Stock[Booked_Car_Name]["Quantity"] -= Booked_Car_Qty
                        Sells[Coustomer_Name] = {
                            "Booked Car Name": Booked_Car_Name,
                            "Purchased Date": Purchased_Date,
                            "Paid Amount": Paid_Amount,
                            "Booking Car Qty": Booked_Car_Qty
                        }
                        print("Booking successful.")
                    else:
                        print("Not enough stock for the requested quantity.")
                else:
                    print("Car is out of stock.")
            else:
                print("Car not found in stock.")
        else:
            print("Customer not found.")

    elif user_input_choice == 4:
        print("-" * 50)
        print("Stock Details:")
        for car_name, details in Car_Stock.items():
            print("Car Name:          ||", car_name)
            print("Manufact:Company : ||", details["Car Company"])
            print("Car Model:         ||", details["Model(Year)"])
            print("Price:             ||", details["Price"])
            print("Quantity:          ||", details["Quantity"])
            print("-" * 50)

        print("Sales Details:")
        for customer_name, details in Sells.items():
            print("Customer Name:     ||", customer_name)
            print("Booked Car:        ||", details["Booked Car Name"])
            print("Purchased Date:    ||", details["Purchased Date"])
            print("Paid Amount:       ||", details["Paid Amount"])
            print("Quantity:          ||", details["Booking Car Qty"])
            print("-" * 50)

    elif user_input_choice == 5:
        print("Exiting the system...")
        break