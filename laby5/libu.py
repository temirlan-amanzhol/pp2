#1
import re
pattern = r'a[b]*'
string = 'ab'
match = re.match(pattern, string)
print(match.group() if match else "No match")



#2
pattern = r'ab{2,3}'  
string = 'abb'        
match = re.match(pattern, string)  
print(match.group() if match else "No match")

#3
pattern = r'[a-z]+_[a-z]+'
string = 'hello_world'
match = re.match(pattern, string)
print(match.group() if match else "No match")

#4
pattern = r'[A-Z][a-z]+'
string = 'Jokey'
match = re.match(pattern, string)
print(match.group() if match else "No match")

#5
pattern = r'a.*b'
string = 'abc'
match = re.match(pattern, string)
print(match.group() if match else "No match")

#6
pattern = r'[ ,.]'
string = 'Hello, world. Welcome!'
replaced_string = re.sub(pattern, ":", string)
print(replaced_string)

#7
pattern = r'(_\w)'
string = 'snake_case_example'
camel_case = re.sub(pattern, lambda match: match.group(1)[1:].upper(), string)
print(camel_case)

#8
pattern = r'([A-Z][a-z]*)'
string = 'HeyMan'
result = re.findall(pattern, string)
print(" ".join(result))

#9
pattern = r'([A-Z])'
string = 'YoYO'
result = re.sub(pattern, r' \1', string)
print(result)

#10
pattern = r'([a-z])([A-Z])'
string = 'camelCaseString'
snake_case = re.sub(pattern, r'\1_\2', string).lower()
print(snake_case)
