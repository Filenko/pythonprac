
# class Rectangle: 

# 	rectcnt = 0

# 	def __init__(self,x1,y1,x2,y2):
	  
# 	    self.x1 = x1       
# 	    self.y1 = y1
# 	    self.x2 = x2
# 	    self.y2 = y2
# 	    Rectangle.rectcnt += 1
# 	    self.__dict__[f"rect_{self.rectcnt}"] = self.rectcnt

# 	def __abs__(self):
# 		return (self.y2-self.y1)*(self.x2-self.x1)
# 	def __str__(self):
# 		return f"()"
# 	def __lt__(self, other):
# 		return abs(self) < abs(other)
# 	def __eq__(self, other):
# 		return abs(self) == abs(other)
# 	def __mul__(self, other):
# 		return Rectangle(self.x1 * other, self.y1 * other,self.x2 * other,self.y2 * other)
# 	__rmul__ = __mul__
# 	def __getitem__(self, ind):
# 		return ((self.x1,self.y1),(self.x1,self.y2),(self.x2,self.y2),(self.x2,self.y1))[ind]


# class C:

# 	def __getattr__(self, attr):
# 		if attr.startswith("a"):
# 			return attr[1:]
# 		else:
# 			return self.__dict__[attr]

class OM:

	dict = {}

	def __getattr__(self, name):
		if "_" + name in self.__dict__:
			return OM.dict[name]
		else:
			return self.__dict__[f"_{name}"]

	def __setattr__(self,name,value):	
		if name not in OM.dict:
			OM.dict[name] = 0
		OM.dict[name] += 1
		self.__dict__[f"_{name}"] = 1

	def __delattr__(self, name):
		if "_" + name in self.__dict__:
			OM.dict[name] -= 1
			del self.__dict__[f"_{name}"]

		
				
		

		
			

