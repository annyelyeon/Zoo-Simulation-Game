class InsufficientFoodError(Exception):
	"""Raised when there is not enough food stock to consume."""


class Food:
	"""Represent a food item in the zoo simulation."""

	def __init__(self, food_type: str, nutritional_value: float, quantity: float) -> None:
		"""Initialize a food item.

		Args:
			food_type: Type of food, such as grass or fish.
			nutritional_value: Amount of hunger reduction provided by the food.
			quantity: Current stock in kilograms.
		"""
		self.food_type = food_type
		self.nutritional_value = nutritional_value
		self.quantity = quantity

	@property
	def quantity(self) -> float:
		"""float: Return the current stock quantity in kilograms."""
		return self.__quantity

	@quantity.setter
	def quantity(self, value: float) -> None:
		"""Set the stock quantity.

		Args:
			value: New stock quantity in kilograms.

		Raises:
			ValueError: If value is less than 0.
		"""
		if value < 0:
			raise ValueError("quantity must be >= 0")
		self.__quantity = value

	def consume(self, amount: float) -> None:
		"""Consume a portion of the food stock.

		Args:
			amount: Amount to consume in kilograms.

		Raises:
			InsufficientFoodError: If quantity is less than amount.
		"""
		if amount > self.quantity:
			raise InsufficientFoodError("Not enough food available to consume")
		self.quantity = self.quantity - amount

	def restock(self, amount: float) -> None:
		"""Increase the food stock.

		Args:
			amount: Amount to add in kilograms.

		Raises:
			ValueError: If amount is less than or equal to 0.
		"""
		if amount <= 0:
			raise ValueError("restock amount must be > 0")
		self.quantity = self.quantity + amount

	def is_available(self) -> bool:
		"""Return whether any stock is available.

		Returns:
			True if quantity is greater than 0, otherwise False.
		"""
		return self.quantity > 0

	def __str__(self) -> str:
		"""Return a readable string representation of the food item.

		Returns:
			A formatted description of the food item.
		"""
		return (
			f"{self.food_type.title()} ("
			f"nutritional_value={self.nutritional_value:.1f}, "
			f"stock={self.quantity:.1f}kg)"
		)


class FoodFactory:
	"""Factory for creating preset food items by type."""

	_NUTRITIONAL_VALUES = {
		"grass": 15.0,
		"leaves": 12.0,
		"eucalyptus": 10.0,
		"fish": 25.0,
		"meat": 30.0,
	}

	@classmethod
	def create(cls, food_type: str, quantity: float) -> Food:
		"""Create a food item with a preset nutritional value.

		Args:
			food_type: Type of food to create.
			quantity: Initial stock in kilograms.

		Returns:
			A Food instance with the preset nutritional value.

		Raises:
			ValueError: If food_type is not recognised.
		"""
		normalized_food_type = food_type.lower()
		if normalized_food_type not in cls._NUTRITIONAL_VALUES:
			raise ValueError(f"Unknown food type: {food_type}")
		return Food(
			food_type=normalized_food_type,
			nutritional_value=cls._NUTRITIONAL_VALUES[normalized_food_type],
			quantity=quantity,
		)
