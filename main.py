import tkinter as tk
import random


class GameManager():
	'''
	Backend logic for the game
	'''
	#Easiest Way to quickly switch between id and name
	tome_of_rps_knowledge = {
			0: "Rock",
			1: "Paper",
			2: "Scissors",
			"Rock": 0,
			"Paper": 1,
			"Scissors": 2
	}
	win_label=None
	lose_label=None
	tie_label=None

	def __init__(self):
		self.user_descisions = []
		self.match_history = []

	def _find_weakness(self, id):
		'''
		Finds the weakness of the given choice
		'''
		if id + 1 == 3:
			return 0
		else:
			return id + 1

	def reset(self):
		'''
		Reset all stats and labels
		'''
		self.user_descisions = []
		self.match_history = []
		self.output_label["text"] = "Press any Button"
		self.win_label["text"] = "Wins: 0"
		self.tie_label["text"] = "Ties: 0"
		self.lose_label["text"] = "Losses: 0"

	def set_output_labels(self, main_output, win, tie, lose):
		'''
		Set the Tkinter Label Widgets for the output handler
		'''
		self.output_label = main_output
		self.win_label = win
		self.tie_label = tie
		self.lose_label = lose

	def find_winner(self, user_choice_id, decider_choice_id):
		'''
		Determine the winner of any given match and return the score for the decider
		'''
		if user_choice_id == decider_choice_id:
			return 0
		elif user_choice_id == self._find_weakness(decider_choice_id):
			return -1
		else:
			return 1

	def cheat(self, user_choice_id):
		'''
		Unlike actual RPS, the opponents moves are already known
		'''
		return self._find_weakness(user_choice_id)

	def bogo_rps(self):
		'''
		If one side throws entireley 'random' moves, the game will always end up
		at about a 50/50 win rate
		'''
		return random.choice([0, 1, 2])

	def goofy_statistician(self):
		'''
		People always have prefered moves
		Could propably also make it find patterns but how'd i know
		'''
		stats = {0: 0, 1: 0, 2: 0}

		for i in range(0, len(self.user_descisions[-10:])):
			choice = self.user_descisions[i]
			#The more recent moves are propably more important
			#How'd i know
			stats[choice] += 1 + 0.5 * i

		prefered_choice = max(stats, key=stats.get)
		return self._find_weakness(prefered_choice)

	def smarty_marty(self):
		'''
		If the user just keeps throwing the same move the statistician gets biased
		'''
		return self._find_weakness(self.user_descisions[-1])

	#Takes care of choosing the approach for this round
	def decider(self, user_choice_id):
		'''
		Decides which strategy to use based on user behavior and 'random' chance
		'''
		#If we are losing, we cheat
		if sum(self.match_history) < 0:
			return self.cheat(user_choice_id), "Shady Dude"
		#If the opponent spams the same choice, we take notice
		temp = self.user_descisions[-3:]
		if temp == [user_choice_id] * 3:
			return self.smarty_marty(), "Smarty Marty"
		#Since it's not actually a good algorithm it wont be used all the time
		if len(self.user_descisions) > 3 and random.random() < 0.5:
			return self.goofy_statistician(), "Statistician"
		#Default to random responses
		return self.bogo_rps(), "Bogo Buddy"

	def play(self, user_choice_id):
		'''
		Plays a round, output will be sent straight to the GUI instead of returned
		since this is supposed to be a callback function
		'''
		self.user_descisions.append(user_choice_id)
		decider_choice_id, decider_algo = self.decider(user_choice_id)
		winner = self.find_winner(user_choice_id, decider_choice_id)
		self.match_history.append(winner)
		self.handle_output(winner, user_choice_id, decider_choice_id, decider_algo)

	def handle_output(self, winner, user_choice_id, decider_choice_id, decider_algo):
		'''
		Turn the numbers into human readable output and display it
		'''
		#Technically breaks if ouput is never set
		#But that can never happen in this implementation
		user_choice = self.tome_of_rps_knowledge[user_choice_id]
		decider_choice = self.tome_of_rps_knowledge[decider_choice_id]
		outcome = ("You " + ("won" if winner == -1 else "lost")
							 ) if user_choice_id != decider_choice_id else "It's a tie"
		self.output_label[
				"text"] = f"You chose {user_choice}.\nThe {decider_algo} chose {decider_choice}.\n{outcome}."
		self.win_label["text"] = f"Wins: {self.match_history.count(-1)}"
		self.tie_label["text"] = f"Ties: {self.match_history.count(0)}"
		self.lose_label["text"] = f"Losses: {self.match_history.count(1)}"


class GameMenu(tk.Frame):
	'''
	GUI for the actualy game, holds the buttons and output labels
	'''
	def __init__(self, parent, window):
		tk.Frame.__init__(self, parent)
		self.window = window
		self.configure(bg="green")

		output_lbl = tk.Label(self,
			text="Press any Button",
			bg="purple",
			fg="green",
			width=35,
			height=3,
			font=("Courier", 20, "bold"))
		output_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

		win_lbl = tk.Label(self,
			text="Wins: 0",
			anchor="w",
			bg="purple",
			fg="green",
			width=12,
			font=("Courier", 15, "bold"))
		win_lbl.grid(row=2, column=0, padx=10, pady=10)

		loss_lbl = tk.Label(self,
			text="Losses: 0",
			anchor="w",
			bg="purple",
			fg="green",
			width=12,
			font=("Courier", 15, "bold"))
		loss_lbl.grid(row=2, column=1, padx=10, pady=10)

		tie_lbl = tk.Label(self,
			text="Ties: 0",
			anchor="w",
			bg="purple",
			fg="green",
			width=12,
			font=("Courier", 15, "bold"))
		tie_lbl.grid(row=2, column=2, padx=10, pady=10)

		#Set the output labels before allowing for user input, otherwise there's a non-zero chance of the user somehow pressing the buttons before the labels are set
		self.window.game_mngr.set_output_labels(output_lbl, win_lbl, tie_lbl, loss_lbl)

		self.rock_btn = tk.Button(self,
			text="Rock",
			bg="grey",
			fg="white",
			command=lambda: self.window.game_mngr.play(0))
		self.rock_btn.grid(row=1, column=0, padx=10, pady=10)

		self.paper_btn = tk.Button(self,
			text="Paper",
			bg="white",
			fg="black",
			command=lambda: self.window.game_mngr.play(1))
		self.paper_btn.grid(row=1, column=1, padx=10, pady=10)

		self.scissors_btn = tk.Button(
			self,
			text="Scissors",
			bg="red",
			fg="white",
			command=lambda: self.window.game_mngr.play(2))
		self.scissors_btn.grid(row=1, column=2, padx=10, pady=10)

		self.back_btn = tk.Button(
			self,
			text="Back",
			bg="white",
			fg="black",
			command=lambda: self.window.show_frame("MainMenu"))
		self.back_btn.grid(row=3, column=0, padx=10, pady=10)

		self.reset_btn = tk.Button(self,
			text="Reset",
			bg="white",
			fg="black",
			command=lambda: self.window.game_mngr.reset())
		self.reset_btn.grid(row=3, column=1, padx=10, pady=10)


class MainMenu(tk.Frame):
	'''
	Main Menu screen, just to add a bit of flair
	'''
	def __init__(self, parent, window):
		tk.Frame.__init__(self, parent)
		self.window = window
		self.configure(bg="yellow")
		self.columnconfigure([0, 1, 2], weight=1)
		self.rowconfigure([0, 1, 2, 3], weight=1)

		#Add a Title
		title = tk.Label(self, text="Bogorps")
		title["fg"] = "Blue"
		title["font"] = ("Comic Sans MS", 32, "bold")

		title.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

		#Add the start button
		start_btn = tk.Button(
			self,
			text="Start",
			#Lambda Function, basically just allows for inlining simple functions
			#equal to
			#def showPageOne():
			#	self.window.show_frame("PageOne")
			command=lambda: self.window.show_frame("GameMenu"))
		#Place the Button in the grid
		start_btn.grid(row=1, column=0, padx=10, pady=10)

		#Add the quit button
		quit_btn = tk.Button(self, text="Quit", command=self.window.destroy)
		quit_btn.grid(row=1, column=2, padx=10, pady=10)


class RPSApp(tk.Tk):
	'''
	Main App Class, holds the main frame, the game manager and the frame map
	All Child Frames can access the stuff here
	'''
	#https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028
	def __init__(self):
		tk.Tk.__init__(self)
		mainframe = tk.Frame(self)
		mainframe.pack(side="top", fill="both", expand=True)
		mainframe.configure(bg="green")
		self.game_mngr = GameManager()

		mainframe.grid(column=0, row=0)
		mainframe.grid_rowconfigure(0, weight=1)
		mainframe.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for SubMenu in ([MainMenu, GameMenu]):
			page_name = SubMenu.__name__
			#Creat an instance of the sub menu and just throw it into the mix with the other frames
			frame = SubMenu(mainframe, self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("MainMenu")

	def show_frame(self, page_name):
		'''
		Switch the Displayed Frame by moving it to the front
		'''
		frame = self.frames[page_name]
		frame.tkraise()


if __name__ == "__main__":
	app = RPSApp()
	#If you cant fix it, hide it
	app.resizable(width=False, height=False)
	app.mainloop()
