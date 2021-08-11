# This is a programme created by Karan Sharma

import os 
def preety(path,file,format):
    os.chdir(f'{path}')
    for item in file.readlines():
        for item2 in os.listdir():
            a=item2.split('.')
            if item!=a[0]:
                if a[1] == format:
                    os.rename(f'{a[0]}.png',f'{a[0]}.jpg')
                    print(item2)
                        
                if a[0] !=item:
                    item3=item2.capitalize()
                    os.rename(f'{item2}',f'{item3}')       

    
    print('This programme run sucessfully and Changed all the files name and Renamed them ')

def main():
    while True:
        path=input('Enter the path of the folder which you watned to aliign \n')
        if os.path.isdir(path)==True:
            ignore=open('ignore.txt')
            fileformat='png'
            preety(path,ignore,fileformat)
            break
        else:
            print('Enter a valid Path')

if __name__ == '__main__':
    main()