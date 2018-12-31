from graphics import *

class Pattern_maker:
	"""Needs to give patterns one by one and be able to save state
	into a file to retrieve later"""
	
	# Constructor one: basic (configuration)
	def __init__(self, pattern, rotate, min_nodes, max_nodes, progress_file_name=None):
		if (progress_file_name is None):
			self.pat = Pattern_maker.relativize(pattern)
			self.rotate = rotate
			self.min = min_nodes
			self.max = max_nodes
			self.current = []
		else:
			fh = open(progress_file_name)
			self.pat = fh.readline().strip().split()
			self.rotate = bool(fh.readline())
			self.min = int(fh.readline())
			self.max = int(fh.readline())
			self.current = map(int, list(fh.readline().strip()))
	
	
	@staticmethod
	def create_from_file(filename):
		"""Create a Pattern_maker from a configuration file."""
		return Pattern_maker(None, None, None, progress_file_name=filename)
	
	
	@staticmethod
	def create_from_config(pattern, rotate, min_nodes, max_nodes):
		"""Create a Pattern_maker from user input."""
		return Pattern_maker(pattern, rotate, min_nodes, max_nodes)
	
	@staticmethod
	def relativize(sequence):
		"""Convert an absolute sequence into its relative equivalent."""
		# Convert sequence to points in matrix
		points = [((value-1) % 3, (value-1) / 3) for value in sequence]
		
		# Get relative points
		rel_points = []
		for i in range(1, len(points)):
			rel_points.append((points[i][0] - points[i-1][0], points[i][1] - points[i-1][1]))
		
		# Transform points into sequence
		rel_sequence = []
		for point in rel_points:
			rel_step = ""
			# Get x
			while (point[0] > 0):
				rel_step += "r"
				point = (point[0] - 1, point[1])
			while (point[0] < 0):
				rel_step += "l"
				point = (point[0] + 1, point[1])
			
			# Get y
			while (point[1] > 0):
				rel_step += "f"
				point = (point[0], point[1] - 1)
			while (point[1] < 0):
				rel_step += "b"
				point = (point[0], point[1] + 1)
			
			rel_sequence.append(rel_step)
		return rel_sequence
	
	@staticmethod
	def increment(curr):
		"""Step to the next possible combination of nodes."""
		if (curr == [] or curr is None):
			return None
	
		done_once = False
		
		while (not done_once or curr[-1] in curr[:-1]):
			done_once = True
			curr[-1] += 1

			if (curr[-1] > 9):
				curr = Pattern_maker.increment(curr[:-1])
				if (curr is None):
					return None
				curr.append(1)
		return curr
	
	@staticmethod
	def turn_pattern(pattern):
		"""Turn a relative pattern clockwise."""
		new_pattern = []
		for entry in pattern:
			new_entry = ""
			for letter in entry:
				new_entry += CLOCKWISE_TURN[letter]
			new_pattern.append(new_entry)
		return new_pattern
	
	@staticmethod
	def contains_relative(sequence, pattern, rotate):
		"""
		Check if a sequence contains a relative pattern.
		This pattern may be in any of the four directions possible.
		"""
		# Make sequence relative
		rel_seq = Pattern_maker.relativize(sequence)
		
		# Check if pattern should rotate or not
		if (rotate):
			lst = range(4)
		else:
			lst = range(1)
		
		# Check for substring (4 directions of pattern)
		for _ in lst:
			same = True
			# Check current pattern
			for (x, y) in zip(rel_seq, pattern):
				x = ''.join(sorted(x))
				y = ''.join(sorted(y))
				if (x != y):
					same = False
					break
			# Return if same pattern
			if (same):
				return True
			# Turn pattern otherwise
			pattern = Pattern_maker.turn_pattern(pattern)
		return False
		
	
	def next(self):
		"""Return the next pattern that follows the given parameters."""
		if (self.current is None):
			return None
		
		if (self.current == []):
			self.current = range(1, self.min + 1)
		else:
			self.current = Pattern_maker.increment(self.current)
		
		while (not Pattern_maker.contains_relative(self.current, self.pat, self.rotate)):
			self.current = Pattern_maker.increment(self.current)
			if (self.current == None):
				if (self.min < self.max):
					self.min += 1
					self.current = range(1, self.min + 1)
				else:
					return None
		
		return self.current
	
	
	def save(self, progress_file_name):
		"""Save the progress in the given file."""
		fh = open(progress_file_name, "w")
		fh.write(" ".join(self.pat) + "\n")
		fh.write(str(self.min) + "\n")
		fh.write(str(self.max) + "\n")
		fh.write("".join(map(str, self.current)) + "\n")
	
	
	def print_params(self):
		"""Print the current parameters for the Pattern_maker."""
		print("\nConfiguration:\n")
		print "\tPattern:", self.pat, "\n\tMinimum:", self.min, "\n\tMaximum:", self.max, "\n\tCurrent:", self.current
		print("")



""" ***************************** Global variables **************************** """
WIN = GraphWin("Phone passwords", 410, 500)
POINTS = 	[	Point(100, 300), Point(200, 300), Point(300, 300), 
				Point(100, 200), Point(200, 200), Point(300, 200),
				Point(100, 100), Point(200, 100), Point(300, 100)
			]
CLOCKWISE_TURN = {
	"f": "r",
	"r": "b",
	"b": "l",
	"l": "f"
}


""" ******************************** Functions ******************************** """
def draw_arrow(src, dest):
	"""Draw an arrow from src to dest."""
	l = Line(src, dest)
	l.setArrow("last")
	l.draw(WIN)
	return l

def draw_pattern(pattern):
	"""Draw the given absolute pattern."""
	drawing = []
	for i in range(1, len(pattern)):
		src = POINTS[pattern[i-1] - 1]
		dst = POINTS[pattern[i] - 1]
		drawing.append(draw_arrow(src, dst))
	return drawing
	
def erase_drawing(drawing):
	"""Erase all graphic elements in drawing."""
	for elem in drawing:
		elem.undraw()
		
def get_restrictions():
	"""Get the initial parameters from user."""
	pattern = raw_input("Input pattern (def: none): ")
	rotate = ""
	while (rotate != "y" and rotate != "n"):
		rotate = raw_input("Should the pattern given rotate? (y/n): ")
	min_nodes = raw_input("Input minimum number of nodes (def: 4): ")
	max_nodes = raw_input("Input maximum number of nodes (def: 9): ")
	
	# Check pattern
	if (pattern == ""):
		pattern = []
	else:
		pattern = map(int, list(pattern))
	
	# Check rotation
	if (rotate == "y"):
		rotate = True
	else:
		rotate = False
	
	# Check min nodes
	try:
		min_nodes = int(min_nodes)
		if (min_nodes < 4 or min_nodes > 9):
			min_nodes = 4
	except:
		min_nodes = 4
	
	# Check max nodes
	try:
		max_nodes = int(max_nodes)
		if (max_nodes > 9):
			max_nodes = 9
	except:
		max_nodes = 9
	
	# Check pattern and min relationship
	if (len(pattern) > min_nodes):
		min_nodes = len(pattern)
	
	# Check min and max relationship
	if (max_nodes < min_nodes):
		max_nodes = min_nodes
	
	return (pattern, rotate, min_nodes, max_nodes)



""" ********************************** Main ********************************** """
if __name__ == "__main__":
	# Process configuration
	try:
		pm = Pattern_maker.create_from_file("file.cfg")  # Check if file exists already
		choice = ""
		while (choice != "y" and choice != "n"):
			choice = raw_input("Do you want to continue with previous session? (y/n) ")
		if (choice == "n"):
			raise Exception()  # To go into except
	
	except:
		(pattern, rotate, min_nodes, max_nodes) = get_restrictions()
		pm = Pattern_maker.create_from_config(pattern, rotate, min_nodes, max_nodes)
	
	pm.print_params()
	
	# Print graphic window
	for point in POINTS:
		c = Circle(point, 10)
		c.draw(WIN)
	save_and_exit = Rectangle(Point(100, 400), Point(300, 450))
	save_and_exit.draw(WIN)
	Text(Point(200, 425), "Save and exit").draw(WIN)
	
	# Start showing results
	current = pm.next()
	while (current is not None):
		print(current)
		drawing = draw_pattern(current)
		p = WIN.getMouse()
		erase_drawing(drawing)
		
		# Check if save and exit button has been pressed
		if (p.getX() > save_and_exit.getP1().getX() and p.getX() < save_and_exit.getP2().getX() and
				p.getY() > save_and_exit.getP1().getY() and p.getY() < save_and_exit.getP2().getY()):
			pm.save("file.cfg")
			break
		current = pm.next()
	
	print("Done")
	WIN.close()
