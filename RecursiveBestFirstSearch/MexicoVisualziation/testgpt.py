def ask_parent():
    while True:
        value = input("Cuánto me quieres? Ingresa un valor del 1 al 5: ")
        if value.isdigit() and 1 <= int(value) <= 5:
            return int(value)
        else:
            print("Por favor, ingresa un número del 1 al 5.")

value = ask_parent()
print(f"Tu papá te quiere {value}!")

