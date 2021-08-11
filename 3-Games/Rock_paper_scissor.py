import random

random_number = random.randint(1,100)



def game(you, comp):
    if(you == comp):
        return 0
    if(you == 'r' and comp == 's'):
        return 1
    elif(you == 's' and comp == 'r'):
        return -1
    if(you == 'p' and comp == 's'):
        return -1
    elif(you == 's' and comp == 'p'):
        return 1
    if(you == 'r' and comp == 'p'):
        return -1
    elif(you == 'p' and comp == 'r'):
        return 1


print("Welcome to the Rock, Paper, Scissor Game\n")
you = str(input("Enter 'r' for rock 'p' for paper and 's' for scissor \n"))

if(random_number < 33):
    comp = 'r'
elif(random_number > 33 and random_number < 66):
    comp = 'p'
else:
    comp = 's'

result=game(you, comp)

print("Computer has chosen",comp,"and you have chosen",you)

if(result==0):
    print("Match is draw !\n")
elif(result == 1):
    print("Congratulations you have won the game\n")
else:
    print("Hard luck Next time\n")

print("THANK YOU FOR PLAYING THE GAME\n")