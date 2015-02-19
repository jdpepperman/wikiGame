class WikiNode:
	#create a wikiNode with a name that will be the title of the 
	#wikipedia page it is connected to.
	def __init__(self, name):
		#sets the name of the node
		self.name = name
		#creates the link for the page for the node
		self.link = "https://en.wikipedia.org/wiki/" + name
		#this will hold the name of the page that links to this node
		self.parent = None
		#this will let us know if the page has been visited
		self.visited = False

	#this sets the node's children to be nodes with links to all the 
	#pages this node's page links to
	def getConnections(self):
		#get the html for the page
		response = urllib2.urlopen(self.link)
		html = response.read()

		#the html comes in as single characters.
		#this puts the html in lines that are easier to parse
		htmlLines = []
		lineToAdd = ""
		for char in html:
			if '\n' in char:
				htmlLines.append(lineToAdd)
				lineToAdd = ""
			else:
				lineToAdd = lineToAdd + char

		#this will get the links from the body of the page.
		wikiNodes = []
		#go through each line in the html
		for line in htmlLines:
			#only look at it if its a regular line of text
			if line[:3] == "<p>":
				#while there are more wiki links in the line
				while "href=\"/wiki/" in line:
					#part1 = everything after href="/wiki/
					part1 = line[line.index("href")+6:]
					#part2 = /wiki/the name of the page (hopefully)
					part2 = part1[:part1.index("\"")]
					#print("Part 2: " + part2)
					#if its a wiki link
					if "wiki" == part2[1:5]:
						#name = the name of the page
						name = part2[6:]
						#if the page is a normal page
						if ':' not in name and '#' not in name and '%' not in name:
							#set up the node and add it
							newNode = WikiNode(name)
							newNode.parent = self
							wikiNodes.append(newNode)
					#cut the part we just looked at out of that line so we can check for more links
					line = line[line.index("href")+6:]

		#when we're done, set this array to be the node's children
		return wikiNodes
		#self.children = self.getConnections()

	def setConnections(self):
		self.children = self.getConnections()

class WikiSolver:
	def __init__(self, startPageName, endPageName):
		self.pageDictionary = {}
		self.head = WikiNode(startPageName)
		self.head.setConnections()
		self.solutionNode = None
		self.solved = False

		self.endPage = endPageName

	def breadthSolve(self):
		self.pageDictionary[self.head.name] = self.head
		while not self.solved:
			tempDict = {}
			for node in self.pageDictionary.itervalues():
				if not node.visited and not self.solved:
					###just for looks###
					if output:
						progressString = ""
						temp = node
						while temp != self.head:
							temp = temp.parent
							progressString = temp.name + "->" + progressString
						print(progressString + node.name)
					######
					node.setConnections()
					for child in node.children:
						if not child.name in self.pageDictionary:
							newNode = WikiNode(child.name)
							newNode.parent = node
							tempDict[newNode.name] = newNode
							if child.name == self.endPage:
								self.solutionNode = newNode
								self.solved = True
								break
					node.visited = True
			self.pageDictionary.update(tempDict)

	def depthSolve(self):
		pageArray = [self.head]
		while not self.solved:
			randIndex = random.randint(0,len(pageArray)-1)
			node = pageArray[randIndex]
			if not node.visited and not self.solved:
				###just for looks###
				if output:
					progressString = ""
					temp = node
					while temp != self.head:
						temp = temp.parent
						progressString = temp.name + "->" + progressString
					print(progressString + node.name)
				######
				node.setConnections()
				for child in node.children:
					if not child.name in self.pageDictionary:
						newNode = WikiNode(child.name)
						newNode.parent = node
						pageArray.append(newNode)
						if child.name == self.endPage:
							self.solutionNode = newNode
							self.solved = True
							break
				node.visited = True

	def depthSolve1(self):
		while not self.solved:
			self.solveRecursive(self.head, 0)

	def solveRecursive(self, node, level):
		if output:
			print(str(level) + " " + node.name)
		if not self.solved:
			for child in node.children:
				if child.name == self.endPage:
					newNode = WikiNode(child.name)
					newNode.parent = node
					self.solutionNode = newNode
					if output:
						print("SOLVED")
					self.solved = True

			#pick a random one instead of just the first one
			if not self.solved and len(node.children) > 0:
				randIndex = random.randint(0,len(node.children)-1)
				#print("Index: " + str(randIndex))
				randChild = node.children[randIndex]
				if not self.solved and randChild.name not in self.pageDictionary:
					randChild.setConnections()
					self.pageDictionary[randChild.name] = randChild
					self.solveRecursive(randChild, level+1)
			else:
				pass
		else:
			pass
		


import urllib2
import random
import sys

if len(sys.argv) == 4:
	output = False
	startPageName = sys.argv[1]
	endPageName = sys.argv[2]
	method = [3]
else:
	output = True
	startPageName = raw_input("Start page name: ")
	endPageName = raw_input("End page name: ")
	method = raw_input("Enter 1 for random depth search, 2 for recursive search, or 3 for breadth search: ")

game = WikiSolver(startPageName, endPageName)

if method == "1":
	game.depthSolve()
elif method == "2":
	game.depthSolve1()
else:
	game.breadthSolve()



solutionPath = []
temp = game.solutionNode
while temp.name != startPageName:
	solutionPath.append(temp)
	temp = temp.parent
solutionPath.append(game.head)

solutionString = ""
for node in solutionPath[::-1]:
	solutionString = solutionString + node.name + "-->"
print(solutionString[:-3])
