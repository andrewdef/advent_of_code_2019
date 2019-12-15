import math

class OutOfOreException(Exception):
	pass

class Reagent:
	name = ''
	amount = 0
	
	def __init__(self, name, amount):
		self.name = name
		self.amount = amount

class Reaction:
	reagents = []
	product_name = ''
	product_amount = 0
	
	def __init__(self, product_name, product_amount):
		self.product_name = product_name
		self.product_amount = product_amount
		self.reagents = []
		
	def add_reagent(self, reagent_name, reagent_amount):
		self.reagents.append(Reagent(reagent_name, reagent_amount))

class ReactionBook:
	reactions_book = {}
	
	def init_from_file(self, input_file):
		with open(input_file) as fd:
			for line in fd.readlines():
				product = line.split('=>')[1].strip()
				product_name = product.split(' ')[1].strip()
				product_amount = int(product.split(' ')[0].strip())
				
				reaction = Reaction(product_name, product_amount)
				
				for reagent in line.split('=>')[0].split(','):
					reagent = reagent.strip()
					reagent_amount = int(reagent.split(' ')[0].strip())
					reagent_name = reagent.split(' ')[1].strip()
					
					reaction.add_reagent(reagent_name, reagent_amount)
					
				self.reactions_book[product_name] = reaction
				
	def get_reaction_for(self, product_name):
		return self.reactions_book.get(product_name)
				
class NanoFactory:
	available_chemicals = {}
	consumed_ore = 0
	available_ore = 0
	
	def __init__(self, reactions_book, available_ore):
		self.reactions_book = reactions_book
		self.available_chemicals = {}
		self.consumed_ore = 0
		self.available_ore = available_ore
		
	def consume_ore(self, amount_to_consume):
		if self.available_ore != None:			
			if amount_to_consume > self.available_ore:
				raise OutOfOreException('Out of ore!')
				
			self.available_ore -= amount_to_consume

		self.consumed_ore += amount_to_consume

	def amount_of_chemical_available(self, product_name):
		amount = self.available_chemicals.get(product_name)
		
		if amount == None:
			amount = 0
			
		return amount
	
	def consume_chemical(self, product_name, product_amount):
		amount_available = self.amount_of_chemical_available(product_name)
			
		if product_amount > amount_available:
			raise ValueError(str(product_amount) + ' Units of ' + product_name + ' are more than the amoutn available in store: ' + amount_available)
			
		self.available_chemicals[product_name] -= product_amount
	
	def add_chemical(self, product_name, product_amount):
		if self.available_chemicals.get(product_name) == None:
			self.available_chemicals[product_name] = 0
			
		self.available_chemicals[product_name] += product_amount
	
	def produce_chemical(self, product_name, product_amount):
		reaction = self.reactions_book.get_reaction_for(product_name)
		if reaction == None:
			raise ValueError('No reaction generates ' + product)
			
		reaction_number_of_runs = math.ceil(product_amount / reaction.product_amount)
		for reagent in reaction.reagents:
			needed_amount = reagent.amount * reaction_number_of_runs
			
			if reagent.name == 'ORE':
				self.consume_ore(needed_amount)
				continue
				
			amount_of_chemical_to_produce = needed_amount - self.amount_of_chemical_available(reagent.name)
			if amount_of_chemical_to_produce > 0:
				self.produce_chemical(reagent.name, amount_of_chemical_to_produce)
				
			self.consume_chemical(reagent.name, needed_amount)
			
		self.add_chemical(product_name, reaction.product_amount * reaction_number_of_runs)