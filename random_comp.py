import random

def game_random(p):
	comp = random.randint(1,3)	# computer random 1 ~ 3
	if(p=='scissor'):	# player: scissor
		if(comp==2):	# player win, computer: paper
			result = 'win'
		elif(comp==3):	# player lose, computer: stone
			result = 'lose'
		else:			# tie, computer: scissor
			result = 'fair'
	elif(p=='paper'):	# player: paper
		if(comp==3):	# player win, computer: stone
			result = 'win'
		elif(comp==1):	# player lose, computer: scissor
			result = 'lose'
		else:			# tie, computer: paper
			result = 'fair'
	else:		# player: stone
		if(comp==1):	# player win, computer: scissor
			result = 'win'
		elif(comp==2):	# player lose, computer: paper
			result = 'lose'
		else:			# tie, computer: stone
			result = 'fair'

	if(comp==1):
		comp_txt = 'scissor'
	elif(comp==2):
		comp_txt = 'paper'
	else:
		comp_txt = 'stone'

	return result, comp_txt

# test
# p = 3
# result,comp = game_random(p)
# print(p)
# print(comp)
# print(result)
