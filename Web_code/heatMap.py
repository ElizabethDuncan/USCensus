shades = {
0 : '#FFFAFA', 
0.2 : '#FFCCCC', 
0.4 : '#FF6A6A', 
0.6 : '#FF3333', 
0.8 : '#CD0000', 
1 : '#800000'} 


def makeShades(values):
	shadeList = []
	print values
	currentmax  = max(values)
	print currentmax

	for value in values:
		if currentmax == 0:
			shadeValue = 0
		else:
			shadeValue = value / currentmax
		if shadeValue == 0:
			shadeList.append(0.1)
		if 0 < shadeValue > 0.2:
			shadeList.append(0.3)
		if 0.2 < shadeValue > 0.4:
			shadeList.append(0.5)
		if 0.4 < shadeValue > 0.6:
			shadeList.append(0.5)	
		if 0.6 < shadeValue > 0.8:
			shadeList.append(0.7)
		if 0.8 < shadeValue >= 1:
			shadeList.append(0.9)

	return shadeList