from abc import ABC, abstractmethod

from animal import Animal
from enclosure import Enclosure, EnclosureFullError
from food import Food, FoodFactory, InsufficientFoodError
from visitor import Visitor


class IObserver(ABC):
	"""Observer interface for receiving animal health alerts."""

	@abstractmethod
	def update(self, animal_name: str, health: float) -> None:
		"""Receive an animal health update.

		Args:
			animal_name: Name of the animal with a health update.
			health: Current health value of the animal.
		"""
		pass


class Manager(IObserver):
	"""Concrete observer that records and prints health alerts."""

	def __init__(self, name: str) -> None:
		"""Initialize a manager observer.

		Args:
			name: Manager name.
		"""
		self.__name = name
		self._alerts: list[str] = []

	def update(self, animal_name: str, health: float) -> None:
		"""Store and print a formatted health alert.

		Args:
			animal_name: Name of the animal with critical health.
			health: Current health value of the animal.
		"""
		alert = f"[ALERT] {animal_name}'s health is critical: {health:.1f}"
		self._alerts.append(alert)
		print(alert)

	def get_alerts(self) -> list[str]:
		"""Return recorded alert messages.

		Returns:
			List of alert messages.
		"""
		return self._alerts

	def clear_alerts(self) -> None:
		"""Clear all recorded alert messages."""
		self._alerts.clear()


class Zoo:
	"""Zoo subject that maintains observers for health notifications."""

	HEALTH_ALERT_THRESHOLD: float = 20.0

	def __init__(self, name: str, funds: float = 0.0) -> None:
		"""Initialize a zoo with core state containers.

		Args:
			name: Zoo name.
			funds: Initial available funds.
		"""
		self.__name = name
		self.__day = 1
		self._enclosures: dict[str, Enclosure] = {}
		self._food_stock: dict[str, Food] = {}
		self._visitors: list[Visitor] = []
		self._funds = funds
		self.__observers: list[IObserver] = []

	@property
	def name(self) -> str:
		"""str: Return the zoo name."""
		return self.__name

	@property
	def day(self) -> int:
		"""int: Return the current simulation day."""
		return self.__day

	@property
	def funds(self) -> float:
		"""float: Return the current available funds."""
		return self._funds

	def register_observer(self, observer: IObserver) -> None:
		"""Register an observer for health alerts.

		Args:
			observer: Observer instance to register.
		"""
		self.__observers.append(observer)

	def remove_observer(self, observer: IObserver) -> None:
		"""Remove a registered observer.

		Args:
			observer: Observer instance to remove.

		Raises:
			ValueError: If observer is not registered.
		"""
		if observer not in self.__observers:
			raise ValueError("Observer not found")
		self.__observers.remove(observer)

	def _notify_observers(self, animal_name: str, health: float) -> None:
		"""Notify all observers of a health update.

		Args:
			animal_name: Name of the animal.
			health: Current health value.
		"""
		for observer in self.__observers:
			observer.update(animal_name, health)

	def add_enclosure(self, enclosure: Enclosure) -> None:
		"""Add an enclosure to the zoo.

		Args:
			enclosure: Enclosure instance to add.

		Raises:
			ValueError: If the enclosure id already exists.
		"""
		enclosure_id = enclosure.enclosure_id
		if enclosure_id in self._enclosures:
			raise ValueError(f"Enclosure '{enclosure_id}' already exists")
		self._enclosures[enclosure_id] = enclosure

	def place_animal(self, animal: Animal, enclosure_id: str) -> None:
		"""Place an animal into a target enclosure.

		Args:
			animal: Animal to place.
			enclosure_id: Target enclosure id.

		Raises:
			KeyError: If enclosure_id does not exist.
		"""
		if enclosure_id not in self._enclosures:
			raise KeyError(f"Enclosure '{enclosure_id}' not found")
		self._enclosures[enclosure_id].add_animal(animal)

	def buy_food(self, food_type: str, quantity: float, cost: float) -> None:
		"""Buy food stock for the zoo.

		Args:
			food_type: Food type to buy.
			quantity: Quantity to purchase.
			cost: Purchase cost.

		Raises:
			ValueError: If available funds are less than cost.
		"""
		if self._funds < cost:
			raise ValueError("Insufficient funds to buy food")

		if food_type in self._food_stock:
			self._food_stock[food_type].restock(quantity)
		else:
			self._food_stock[food_type] = FoodFactory.create(food_type, quantity)

		self._funds -= cost

	def feed_enclosure(self, enclosure_id: str, food_type: str) -> None:
		"""Feed all animals in a specific enclosure using a food stock item.

		Args:
			enclosure_id: Enclosure id to feed.
			food_type: Food type to use.

		Raises:
			KeyError: If enclosure_id or food_type is not found.
		"""
		if enclosure_id not in self._enclosures:
			raise KeyError(f"Enclosure '{enclosure_id}' not found")
		if food_type not in self._food_stock:
			raise KeyError(f"Food type '{food_type}' not found")

		enclosure = self._enclosures[enclosure_id]
		food_item = self._food_stock[food_type]
		enclosure.feed_all(food_item)

	def admit_visitor(self, visitor: Visitor, ticket_price: float) -> None:
		"""Admit a visitor and collect ticket revenue.

		Args:
			visitor: Visitor to admit.
			ticket_price: Ticket price to charge.
		"""
		visitor.spend(ticket_price)
		self._funds += ticket_price
		self._visitors.append(visitor)

	def collect_donation(self, visitor: Visitor, amount: float) -> None:
		"""Collect a donation from a visitor.

		Args:
			visitor: Donating visitor.
			amount: Donation amount.
		"""
		donated_amount = visitor.donate(amount)
		self._funds += donated_amount

	def tick(self) -> None:
		"""Advance the simulation by one day.

		Order of operations:
		1. Update all enclosures.
		2. Notify observers for animals at or below health alert threshold.
		3. Increment day.
		4. Print day-start message.
		"""
		for enclosure in self._enclosures.values():
			enclosure.update_all()

		for enclosure in self._enclosures.values():
			for animal in enclosure.get_animals():
				if animal.is_critical(self.HEALTH_ALERT_THRESHOLD):
					self._notify_observers(animal.name, animal._health)

		self.__day += 1
		print(f"=== Day {self.__day} begins ===")
		
	def get_enclosure(self, enclosure_id: str) -> Enclosure:
		"""Return an enclosure by id.

		Args:
			enclosure_id: Id of the enclosure to retrieve.

		Returns:
			The Enclosure instance with the specified id.

		Raises:
			KeyError: If enclosure_id does not exist.
		"""
		if enclosure_id not in self._enclosures:
			raise KeyError(f"Enclosure '{enclosure_id}' not found")
		return self._enclosures[enclosure_id]

	def get_status(self) -> str:
		"""Return a multi-line summary of zoo state.

		Returns:
			A formatted multi-line status string.
		"""
		total_animals = sum(
			enclosure.animal_count for enclosure in self._enclosures.values()
		)
		return (
			f"Zoo: {self.__name}\n"
			f"Day: {self.__day}\n"
			f"Funds: ${self._funds:.2f}\n"
			f"Enclosures: {len(self._enclosures)}\n"
			f"Total animals: {total_animals}\n"
			f"Total visitor: {len(self._visitors)}"
		)
