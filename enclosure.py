from abc import ABC, abstractmethod

from animal import Animal
from animal import IncompatibleFoodError
from food import Food
from food import InsufficientFoodError


class ICleanable(ABC):
	"""Interface for objects that can be cleaned and report cleanliness."""

	@abstractmethod
	def clean(self) -> None:
		"""Clean the object."""
		pass

	@abstractmethod
	def get_cleanliness(self) -> float:
		"""Return the current cleanliness value.

		Returns:
			The cleanliness value as a float.
		"""
		pass


class EnclosureFullError(Exception):
	"""Raised when an animal is added to a full enclosure."""


class Enclosure(ICleanable):
	"""Represent a zoo enclosure that houses animals of a given habitat type."""

	def __init__(
		self,
		enclosure_id: str,
		habitat_type: str,
		max_capacity: int,
		cleanliness: float = 100.0,
		is_open: bool = True,
	) -> None:
		"""Initialize an enclosure.

		Args:
			enclosure_id: Identifier for the enclosure.
			habitat_type: Habitat category for the enclosure.
			max_capacity: Maximum number of animals the enclosure can hold.
			cleanliness: Initial cleanliness value in the range 0.0 to 100.0.
			is_open: Whether the enclosure is currently open.
		"""
		self.__enclosure_id = enclosure_id
		self.__habitat_type = habitat_type
		self.__max_capacity = max_capacity
		self._animals: list[Animal] = []
		self._cleanliness = cleanliness
		self._is_open = is_open

	@property
	def enclosure_id(self) -> str:
		"""str: Return the enclosure identifier."""
		return self.__enclosure_id

	@property
	def habitat_type(self) -> str:
		"""str: Return the enclosure habitat type."""
		return self.__habitat_type

	@property
	def max_capacity(self) -> int:
		"""int: Return the maximum enclosure capacity."""
		return self.__max_capacity

	@property
	def animal_count(self) -> int:
		"""int: Return the number of animals currently in the enclosure."""
		return len(self._animals)

	def get_animals(self) -> list[Animal]:
		"""Return a copy of the animals currently in the enclosure.

		Returns:
			A shallow copy of the enclosure animal list.
		"""
		return list(self._animals)

	def add_animal(self, animal: Animal) -> None:
		"""Add an animal to the enclosure.

		Args:
			animal: Animal to add.

		Raises:
			ValueError: If the enclosure is closed.
			EnclosureFullError: If the enclosure is already at capacity.
		"""
		if not self._is_open:
			raise ValueError("Cannot add animals to a closed enclosure")
		if self.animal_count >= self.__max_capacity:
			raise EnclosureFullError("Enclosure is full")
		self._animals.append(animal)

	def remove_animal(self, animal: Animal) -> None:
		"""Remove an animal from the enclosure.

		Args:
			animal: Animal to remove.

		Raises:
			ValueError: If the animal is not currently in the enclosure.
		"""
		if animal not in self._animals:
			raise ValueError("Animal is not in this enclosure")
		self._animals.remove(animal)

	def feed_all(self, food_item: Food) -> None:
		"""Feed all animals in the enclosure.

		Each successful feeding consumes 1.0 kg of food stock. Incompatible food
		is reported and skipped for the affected animal.

		Args:
			food_item: Food item to offer to all animals.

		Raises:
			InsufficientFoodError: If the food stock is depleted during feeding.
		"""
		for index, animal in enumerate(self._animals):
			if not food_item.is_available():
				raise InsufficientFoodError("Food ran out during feeding")

			try:
				animal.eat(food_item)
			except IncompatibleFoodError:
				print(
					f"Warning: {animal.name} cannot eat {food_item.food_type} "
					f"in enclosure {self.__enclosure_id}."
				)
				continue

			food_item.consume(1.0)

			if food_item.quantity == 0 and index < len(self._animals) - 1:
				raise InsufficientFoodError("Food ran out during feeding")

	def update_all(self) -> None:
		"""Update the status of every animal and reduce cleanliness accordingly."""
		for animal in self._animals:
			animal.update_status()
			self._cleanliness = max(0.0, self._cleanliness - 5.0)

	def clean(self) -> None:
		"""Clean the enclosure and restore cleanliness to 100.0."""
		self._cleanliness = 100.0
		print(f"Enclosure {self.__enclosure_id} has been cleaned.")

	def get_cleanliness(self) -> float:
		"""Return the current cleanliness value.

		Returns:
			The current cleanliness as a float.
		"""
		return self._cleanliness

	def get_status(self) -> str:
		"""Return a summary of the enclosure state.

		Returns:
			A formatted status string.
		"""
		return (
			f"Enclosure {self.__enclosure_id} [{self.__habitat_type}] - "
			f"{self.animal_count}/{self.__max_capacity} animals, "
			f"cleanliness: {self._cleanliness:.1f}%"
		)

	def __str__(self) -> str:
		"""Return a human-readable string representation of the enclosure.

		Returns:
			A formatted enclosure summary string.
		"""
		return (
			f"Enclosure {self.__enclosure_id} [{self.__habitat_type}] — "
			f"{self.animal_count}/{self.__max_capacity} animals, "
			f"cleanliness: {self._cleanliness:.1f}%"
		)
