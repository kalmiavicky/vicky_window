#自動開檔案
with open('names.txt',encoding='utf-8') as file:
    content:str = file.read()  #回傳字串
#print(content)   #加print(content)可以列印出換行的名子
names:list[str]=content.split() #算出有幾個名字 
len(names)                       #算出有幾個名字  
for name in names:
    print(name)
