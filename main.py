import random

from zoo import Zoo, Manager
from animal import Kangaroo, Koala, Eagle, Penguin
from enclosure import Enclosure, EnclosureFullError
from food import FoodFactory, InsufficientFoodError
from visitor import Visitor
from system import ResourceManager, InsufficientFundsError


def setup_zoo() -> Zoo:
	"""Create a fully configured zoo instance.

	Returns:
		A Zoo object with manager, enclosures, animals, and starter food.
	"""
	zoo = Zoo("OzZoo", funds=1000.0)

	manager = Manager("Head Keeper")
	zoo.register_observer(manager)

	enclosure_e01 = Enclosure("E01", "savanna", max_capacity=5)
	enclosure_e02 = Enclosure("E02", "arctic", max_capacity=4)
	enclosure_e03 = Enclosure("E03", "forest", max_capacity=4)

	zoo.add_enclosure(enclosure_e01)
	zoo.add_enclosure(enclosure_e02)
	zoo.add_enclosure(enclosure_e03)

	skippy = Kangaroo("Skippy", jump_height=2.5, mob_size=3)
	bluey = Koala("Bluey", eucalyptus_tolerance=0.8)
	wedge = Eagle(
		"Wedge",
		wingspan=210.0,
		feather_colour="brown",
		max_altitude=1800.0,
		territory_size=5.0,
		hunting_skill=0.9,
	)
	pingu = Penguin(
		"Pingu",
		wingspan=60.0,
		feather_colour="black and white",
		running_speed=2.5,
		swim_speed=8.0,
		colony_size=12,
	)

	zoo.place_animal(skippy, "E01")
	zoo.place_animal(bluey, "E03")
	zoo.place_animal(wedge, "E01")
	zoo.place_animal(pingu, "E02")

	zoo.buy_food("grass", quantity=20.0, cost=40.0)
	zoo.buy_food("eucalyptus", quantity=15.0, cost=30.0)
	zoo.buy_food("meat", quantity=10.0, cost=50.0)
	zoo.buy_food("fish", quantity=20.0, cost=40.0)

	return zoo


def print_menu() -> None:
	"""Print the OzZoo command-line menu."""
	print("=== OzZoo Manager ===")
	print("1. View zoo status")
	print("2. Feed enclosure")
	print("3. Clean enclosure")
	print("4. Admit visitor")
	print("5. View financial summary")
	print("6. Advance day")
	print("7. View animal status")
	print("8. Quit")


def main() -> None:
	"""Run the OzZoo command-line management loop."""
	zoo = setup_zoo()
	rm = ResourceManager.get_instance()

	while True:
		print_menu()
		option = input("Choose an option: ").strip()

		try:
			if option == "1":
				print(zoo.get_status())

			elif option == "2":
				enclosure_id = input("Enclosure ID: ").strip()
				food_type = input("Food type: ").strip()
				zoo.feed_enclosure(enclosure_id, food_type)
				print(f"Fed enclosure {enclosure_id} with {food_type}.")

			elif option == "3":
				enclosure_id = input("Enclosure ID: ").strip()
				enclosure = zoo.get_enclosure(enclosure_id)
				enclosure.clean()

			elif option == "4":
				name = input("Visitor name: ").strip()
				ticket_price = float(input("Ticket price: $"))
				visitor = Visitor(
					visitor_id=f"V{random.randint(100, 999)}",
					name=name,
					budget=100.0,
				)
				zoo.admit_visitor(visitor, ticket_price)
				rm.earn(ticket_price, "Ticket sale")
				print(f"Welcome to OzZoo, {name}!")

			elif option == "5":
				print(rm.get_summary())

			elif option == "6":
				zoo.tick()
				rm.reset_daily_totals()

			elif option == "7":
				enclosure_id = input("Enclosure ID: ").strip()
				enclosure = zoo.get_enclosure(enclosure_id)
				for animal in enclosure.get_animals():
					print(animal.get_status())

			elif option == "8":
				print("Thanks for managing OzZoo! Goodbye.")
				break

			else:
				print("Invalid option. Please try again.")

		except KeyError as error:
			print(f"Not found: {error}")
		except ValueError as error:
			print(f"Invalid input: {error}")
		except EnclosureFullError as error:
			print(f"Enclosure error: {error}")
		except InsufficientFundsError as error:
			print(f"Funds error: {error}")
		except InsufficientFoodError as error:
			print(f"Food error: {error}")


if __name__ == "__main__":
	main()
