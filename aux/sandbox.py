name = input("Enter your name: ")
print("Trying to excape to the right sequence")
print("\'\\x1b[A\'")
if name == "Michael":
    print("Hello my Lord!")
elif name == r"'\x1b[A'":
    print("That's the up key")
else:
    print("Yaya")
    print(r"'\x1b[A'" +  f"is not the same as {name}")