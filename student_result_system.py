import pandas as pd
import os

CSV_FILE = "student_results_sem2_extracted.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        print("CSV not found, starting with empty DataFrame.")
        return pd.DataFrame(columns=["roll_no","name","father_name","sgpa","result"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)
    print(f"Data saved to {CSV_FILE}")

def show_all(df):
    if df.empty:
        print("No records to display.")
    else:
        print(df.to_string(index=False))

def search_roll(df):
    roll = input("Enter roll number to search: ").strip()
    rec = df[df["roll_no"].astype(str) == roll]
    if rec.empty:
        print("Record not found.")
    else:
        print(rec.to_string(index=False))

def add_student(df):
    roll = input("Roll No: ").strip()
    if not df[df["roll_no"].astype(str) == roll].empty:
        print("Roll already exists.")
        return df
    name = input("Name: ").strip().title()
    father = input("Father Name: ").strip().title()
    sgpa = float(input("SGPA (0‑10): ").strip())
    result = input("Result (Pass/Re-Appear): ").strip().title()
    new_row = {"roll_no": roll, "name": name, "father_name": father, "sgpa": sgpa, "result": result}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    print("Student added.")
    return df

def update_student(df):
    roll = input("Enter roll number to update: ").strip()
    idx = df.index[df["roll_no"].astype(str) == roll]
    if idx.empty:
        print("Record not found.")
        return df
    i = idx[0]
    print(f"Current record:\n{df.loc[i]}")
    sgpa = float(input("New SGPA (leave blank to skip): ") or df.loc[i,"sgpa"])
    result = input("New Result (leave blank to skip): ") or df.loc[i,"result"]
    df.loc[i,"sgpa"] = sgpa
    df.loc[i,"result"] = result.title()
    print("Record updated.")
    return df

def delete_student(df):
    roll = input("Enter roll number to delete: ").strip()
    before = len(df)
    df = df[df["roll_no"].astype(str) != roll]
    if len(df) < before:
        print("Deleted.")
    else:
        print("Record not found.")
    return df

def menu():
    df = load_data()
    while True:
        print("\n------- Student Result Management -------")
        print("1. Show all students")
        print("2. Search by roll number")
        print("3. Add new student")
        print("4. Update SGPA / result")
        print("5. Delete student")
        print("6. Save & exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            show_all(df)
        elif choice == "2":
            search_roll(df)
        elif choice == "3":
            df = add_student(df)
        elif choice == "4":
            df = update_student(df)
        elif choice == "5":
            df = delete_student(df)
        elif choice == "6":
            save_data(df)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
