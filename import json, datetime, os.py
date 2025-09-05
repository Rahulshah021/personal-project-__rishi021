import json, datetime, os

# ---------- File Handling ----------
# Load land data from JSON (if file not found, create default data)
def load_lands():
    if os.path.exists("lands.json"):
        return json.load(open("lands.json"))
    return {"L1": True, "L2": True, "L3": True}   # True = Available, False = Rented

# Save land data back to JSON file
def save_lands(lands):
    json.dump(lands, open("lands.json", "w"), indent=4)

# Save text into a file (used for transactions and invoices)
def save_file(text, filename):
    with open(filename, "a") as f:
        f.write(text + "\n")

# ---------- Invoice ----------
# Create and display invoice for rent/return
def invoice(customer, land, days, penalty=0):
    cost_per_day = 500       # fixed cost per day
    total = days * cost_per_day + penalty
    text = f"""
--- LAND INVOICE ---
Customer: {customer}
Land: {land}
Days: {days}
Cost/Day: Rs.{cost_per_day}
Penalty: Rs.{penalty}
TOTAL: Rs.{total}
---------------------
"""
    # Save invoice as a separate file
    fname = f"invoice_{customer}_{land}.txt"
    save_file(text, fname)

    # Show invoice on screen
    print(text)

# ---------- Main Program ----------
lands = load_lands()   # Load existing land data

while True:
    # Menu
    print("\n1. Show Lands  2. Rent  3. Return  4. Exit")
    ch = input("Choice: ")

    # Show all lands with status
    if ch == "1":
        for l, free in lands.items():
            print(l, "Available" if free else "Rented")

    # Rent a land
    elif ch == "2":
        c = input("Customer: ")
        l = input("Land ID: ")
        d = int(input("Days: "))

        if lands.get(l, False):    # if available
            lands[l] = False       # mark as rented
            save_lands(lands)      # update JSON file
            save_file(f"{c} rented {l} for {d} days", "transactions.txt")
            invoice(c, l, d)       # generate invoice
        else:
            print("Not available!")

    # Return a land
    elif ch == "3":
        c = input("Customer: ")
        l = input("Land ID: ")

        if l in lands and not lands[l]:   # if rented
            lands[l] = True
            save_lands(lands)

            # Ask for late days, penalty = Rs.200 per day
            penalty = int(input("Late days (0 if none): ")) * 200
            save_file(f"{c} returned {l} with penalty Rs.{penalty}", "transactions.txt")

            # For simplicity, assume always rented for 5 days
            invoice(c, l, 5, penalty)
        else:
            print("Invalid return!")

    # Exit program
    elif ch == "4":
        print("Goodbye!")
        break
