lines = open("static/js/test.min.js").readlines()[0].split(";")
#一般压缩后的文件所有代码都在一行里
#视情况设定索引，我的情况时第0行是源代码。
indent = 0
formatted = []
for line in lines:
  newline = []
  for char in line:
    newline.append(char)
    if char=='{': #{ 是缩进的依据
      indent+=1
      newline.append("\n")
      newline.append("\t"*indent)
    if char=="}":
      indent-=1
      newline.append("\n")
      newline.append("\t"*indent)
  formatted.append("\t"*indent+"".join(newline))
open("formated.js","w").writelines(";\n".join(formatted))