import sys # access variables by the interpreter

def count_request_codes(): # a function, that initialize the three variables to zero
    count_200 = 0
    count_302 = 0
    count_404 = 0

    for line in sys.stdin: # starts a loop that iterates over the input 
        if '200' in line:
            count_200 += 1
        elif '302' in line:
            count_302 += 1
        elif '404' in line:
            count_404 += 1

    print(f"Number of requests with code 200: {count_200}")
    print(f"Number of requests with code 302: {count_302}")
    print(f"Number of requests with code 404: {count_404}")
if __name__ == '__main__':
    count_request_codes()