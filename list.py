input_str='aabbccdda'
# out=a2b2c2d2a1
list_a=[]
count=1
for i in range(1,len(input_str)+1):
    if len(input_str)>i:
        if input_str[i-1]==input_str[i]:
            list_a.append(input_str[i])
            count+=1
        else:
            list_a.append(str(count))
            count=1
    else:
        list_a.append(input_str[i-1])
        list_a.append(str(count))
print(''.join(list_a))

        



    #     input[0]==int(i+1)
