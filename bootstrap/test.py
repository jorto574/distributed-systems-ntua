from flask import session

def test():
    my_state = session['state']
    print(my_state) 

if __name__ == '__main__':
    test()