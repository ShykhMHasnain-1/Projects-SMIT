Car_Stock = {}
Coustomer = {}
Sells = {}

while True:
    print("-"*50)
    print(" "*10,"Showroom Management System")
    print("-"*50)
    print("1.Stock Management\n2.Coustmer Managment\n3.Billing System\n4.Report\n5.Exit")
    print("-"*50)
    user_input_choice = int(input("Enter The Choice(1/2/3/4/5):"))
    print("-"*50)
    if user_input_choice == 1:
        while True:
            print("1.Add Stock\n2.View Stocks\n3.Update Stocks\n4.Delete Stocks\n5.Exit From S.M")
            user_input_choice_SM = int(input("Enter The Choice(1/2/3/4/5):"))
            print("-"*50)
            if user_input_choice_SM == 1:
                Car_Name = input("Enter The Car Name:")
                Car_Company = input("Enter The Car Name:")
                Car_Model = int(input("Enter The Car Name:"))
                Car_Price = int(input("Enter The Car Name:"))
                Car_Qty = int(input("Enter The Car Name:"))
                Car_Stock = {
                    "Car Name" : Car_Name,
                    "Car Company" : Car_Company,
                    "Model(Year)" : Car_Model,
                    "Price" : Car_Price,
                    "Quantity" : Car_Qty
                }
                print("------- Stock Added Succesfully...!!! -------")
            elif user_input_choice_SM == 2:
                for stocks in Car_Stock:
                    print("Car Name:          ||",Car_Stock.get("Car Name"))
                    print("Manufact:Company : ||",Car_Stock.get("Car Company"))
                    print("Car Model:         ||",Car_Stock.get("Model(Year)"))
                    print("Price:             ||",Car_Stock.get("Price"))
                    print("Quatity:           ||",Car_Stock.get("Quantity"))
                    print("*"*50)
            elif user_input_choice_SM == 3:
                Car_Name_To_Check = input("Enter The Car Name To Update: ")
                if Car_Name_To_Check == Car_Stock["Car Name"]:
                    while True:
                        print("1.Update Car Name\n2.Update Car Company\n3.Update Car Model(M.Year)\n4.Update Car Price\n5.Update car Quantity")
                        user_input_choice_update = int(input("Enter Your Choice:(1/2/3/4/5)"))
                        if user_input_choice_update == 1:
                            upd_car_name = input("Enter The Update Car Name: ")
                            Car_Stock["Car Name"] = upd_car_name
                            print("------- Info Update Successfully!!! -------")
                            print("Car Name:",Car_Stock.get("Car Name"))
                            print("Company: ",Car_Stock.get("Car Company"))
                            print("Model(Year): ",Car_Stock.get("Model(Year)"))
                            print("Price :",Car_Stock.get("Price"))
                            print("Quantity: ",Car_Stock.get("Quantity"))
                            print("+"*50)

                        elif user_input_choice_update == 2:
                            upd_car_comp = input("Enter The Update Car Name: ")
                            Car_Stock["Car Company"] = upd_car_comp
                            print("------- Info Update Successfully!!!")
                            print("Car Name:",Car_Stock.get("Car Name"))
                            print("Company: ",Car_Stock.get("Car Company"))
                            print("Model(Year): ",Car_Stock.get("Model(Year)"))
                            print("Price :",Car_Stock.get("Price"))
                            print("Quantity: ",Car_Stock.get("Quantity"))
                            print("+"*50)

                        elif user_input_choice_update == 3:
                            upd_car_model = input("Enter The Update Car Name: ")
                            Car_Stock["Model(Year)"] = upd_car_model
                            print("------- Info Update Successfully!!!")
                            print("Car Name:",Car_Stock.get("Car Name"))
                            print("Company: ",Car_Stock.get("Car Company"))
                            print("Model(Year): ",Car_Stock.get("Model(Year)"))
                            print("Price :",Car_Stock.get("Price"))
                            print("Quantity: ",Car_Stock.get("Quantity"))
                            print("+"*50)

                        elif user_input_choice_update == 4:
                            upd_car_price = input("Enter The Update Car Name: ")
                            Car_Stock["Price"] = upd_car_price
                            print("------- Info Update Successfully!!!")
                            print("Car Name:",Car_Stock.get("Car Name"))
                            print("Company: ",Car_Stock.get("Car Company"))
                            print("Model(Year): ",Car_Stock.get("Model(Year)"))
                            print("Price :",Car_Stock.get("Price"))
                            print("Quantity: ",Car_Stock.get("Quantity"))
                            print("+"*50)

                        elif user_input_choice_update == 5:
                            upd_car_Qty = input("Enter The Update Car Quantity: ")
                            Car_Stock["Quantity"] = upd_car_Qty
                            print("------- Info Update Successfully!!! ------")
                            print("Car Name:",Car_Stock.get("Car Name"))
                            print("Company: ",Car_Stock.get("Car Company"))
                            print("Model(Year): ",Car_Stock.get("Model(Year)"))
                            print("Price :",Car_Stock.get("Price"))
                            print("Quantity: ",Car_Stock.get("Quantity"))
                            print("+"*50)

                            print("1.Want To Update Same Car\n21.Want To Update Another Car\n.3.Exit From Update Mode")
                            user_input_choice_upd_S_O = int(input("Enter Choice: "))
                            if user_input_choice_upd_S_O == 1:
                                continue
                            elif user_input_choice_upd_S_O == 2:
                                break
                            elif user_input_choice_upd_S_O == 3:
                                break
            elif user_input_choice_SM == 4:      
                Car_Name_To_Delete = input("Enter The Car Name To Delete: ")
                if Car_Name_To_Delete in Car_Stock:
                    del Car_Stock[Car_Name_To_Delete]
                    print(f"Item: {Car_Name_To_Delete} is removed From Stock")
            elif user_input_choice_SM == 5:
                break
    elif user_input_choice == 2:
        C_Name = input("Enter The Customer Name: ")
        C_CNIC = input("Enter The Customer Name: ")
        C_Con_Numer = input("Enter The Customer Name: ")
        C_Address = input("Enter The Customer Name: ")

        Coustomer.update({"Customer Name:        ":C_Name,
                          "Customer CNIC:        ":C_CNIC,
                          "Coustomer Con Numeber:":C_Con_Numer,
                          "Coustomer Address:    ":C_Address
                          })
    elif user_input_choice == 3:
        Coustomer_Name = input("Enter Customer Name:")
        if Coustomer_Name in Coustomer["Customer Name"]:
            Booked_Car_Name = input("Enter The Booked Car Name: ")
            if Booked_Car_Name in Car_Stock["Car Name"] and Booked_Car_Name in Car_Stock["Quantity"] != 0:
                Purchased_Date = input("Enter Booking Date:")
                Paid_Amount = int(input("Enter Booking Date:"))
                Booked_Car_Qty = int(input("Enter Booked Car Qty:"))
                len(Booked_Car_Name in Car_Stock["Car Name"])-1
                Sells.update({"Customer Name:   ",Coustomer_Name,
                              "Booked Car Name: ",Booked_Car_Name,
                              "Purchased Date:    ",Purchased_Date,
                              "Paid Amount:  ",Paid_Amount,
                              "Booking Car Qty: ",Booked_Car_Qty
                              })
    elif user_input_choice == 4:
        print("+"*50)
        print("Car Name:          ||",Car_Stock.get("Car Name"))
        print("Manufact:Company : ||",Car_Stock.get("Car Company"))
        print("Car Model:         ||",Car_Stock.get("Model(Year)"))
        print("Price:             ||",Car_Stock.get("Price"))
        print("Quatity:           ||",Car_Stock.get("Quantity"))
        print("+"*50)

        print("Sells")
        print("+"*50)
        print("Car Name:             ||",Sells.get("Booked Car Name"))
        print("Booked By:            ||",Sells.get("Customer Name"))
        print("Purchased Date:       ||",Sells.get("Purchased Date"))
        print("Amount:               ||",Sells.get("Paid Amount"))
        print("Qty:                  ||",Sells.get("Booking Car Qty"))
        print("+"*50)


