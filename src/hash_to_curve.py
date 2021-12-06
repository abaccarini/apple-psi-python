import sys
import libnum

p=149
startval=10

if (len(sys.argv)>1):
	startval=int(sys.argv[1])

if (len(sys.argv)>2):
	p=int(sys.argv[2])

def findit(start,p):
  x=start
  while (True):
    y_2=x**3+7
    if (libnum.has_sqrtmod(y_2,{p:1} )):
      y=next(libnum.sqrtmod(y_2,{p:1}))
      return(x,y)
    x=x+1
  
print("Elliptic curve is:\t\ty^2=x^3+7")
print("Finding elliptic point closes to:\t",startval)
print("Prime number:\t\t\t",p)
print()
print("Closest point is:\t\t",findit(startval,p))