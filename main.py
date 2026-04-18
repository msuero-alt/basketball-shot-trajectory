import subprocess

while True:
    print("\n=== TTD System ===")
    print("1. Track Ball")
    print("2. Map Court")
    print("3. Plot Trajectory")
    print("4. Exit")

    choice = input("Select option: ")

    if choice == "1":
        subprocess.run(["python", "run_ball.py"])
    elif choice == "2":
        subprocess.run(["python", "run_court.py"])
    elif choice == "3":
        subprocess.run(["python", "run_plot.py"])
    elif choice == "4":
        break
