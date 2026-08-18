import os

print("Installing requirements")
os.system("pip install -r requirements.txt")

if not os.path.exists("storage/QaA.txt"):
    with open("storage/QaA.txt", mode="w") as file:
        file.write("")
else:
    print("you already have QaA.txt file")


if not os.path.exists("storage/QuestionRequests.txt"):
    with open("storage/QuestionRequests.txt", mode="w") as file:
        file.write("")
else:
    print("you already have QuestionRequests.txt file")


if not os.path.exists(".env"):
    DISCORD_TOKEN = input("Please provide your discord token: ")
    with open("storage/storage/QuestionRequests.txt", mode="w") as file:
        file.write(f"DISCORD_TOKEN={DISCORD_TOKEN}")
else:
    print("you already have .env file")