# records = [["chi", 20.0], ["beta", 30.0], ["alpha", 30.0]]
# sorted(records)
# records.sort()
# for i, score in records:
#     print (i)
    
# def split(line):
#    list_string = line.split(" ")
   
#    return list_string

# def join(line):
#     join_string = "-".join(line)
#     return join_string

# if __name__ == '__main__':
#     string = 'this is a string'
#     list_string = split(string) 
#     print(list_string) 
    
#     new_string = join(list_string)
#     print(new_string)
    
    
# n = int(input())
# for i in range(1, n+1):
#     print (i**2)

# matrix = [[j for j in range(5)] for i in range(4)]
 
# print(matrix)


# multiple_of_2 = []

# for i in range (1, 12+1):
#     multiple_of_2.append(i * 2)
    
   
# print(multiple_of_2)
   
# if __name__ == '__main__':
#     N = int(input())
#     empty = []
#     conv = []
    
#     for i in range(N):
#         x = input().split()
#         empty.append(x)
#         print(empty)
word=  "ABCDCDC"
sub="CDC"
count=0

for i in range(len(word)):
    if word[i]==sub[0]:
      print(word[i])
      if sub== word[i:(i+len(sub))]:
        count+=1
# print(count)


