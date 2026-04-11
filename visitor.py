from enclosure import Enclosure


class Visitor:
	"""Represent a zoo visitor and their interactions with enclosures."""

	def __init__(
		self,
		visitor_id: str,
		name: str,
		budget: float,
		satisfaction: float = 50.0,
	) -> None:
		"""Initialize a visitor.

		Args:
			visitor_id: Unique visitor identifier.
			name: Visitor display name.
			budget: Available spending budget.
			satisfaction: Initial satisfaction value from 0.0 to 100.0.
		"""
		self.__visitor_id = visitor_id
		self.__name = name
		self._satisfaction = satisfaction
		self._budget = budget
		self._visited_enclosures: list[str] = []

	@property
	def visitor_id(self) -> str:
		"""str: Return the unique visitor identifier."""
		return self.__visitor_id

	@property
	def name(self) -> str:
		"""str: Return the visitor name."""
		return self.__name

	@property
	def satisfaction(self) -> float:
		"""float: Return the current satisfaction level."""
		return self._satisfaction

	@property
	def budget(self) -> float:
		"""float: Return the remaining budget."""
		return self._budget

	def visit_enclosure(self, enclosure: Enclosure) -> None:
		"""Record a visit and update satisfaction based on enclosure cleanliness.

		Args:
			enclosure: Enclosure being visited.
		"""
		self._visited_enclosures.append(enclosure.enclosure_id)

		cleanliness = enclosure.get_cleanliness()
		if cleanliness >= 80:
			self._satisfaction += 10
		elif cleanliness >= 50:
			self._satisfaction += 5
		else:
			self._satisfaction -= 10

		self._satisfaction = max(0.0, min(100.0, self._satisfaction))

	def spend(self, amount: float) -> None:
		"""Spend part of the visitor budget.

		Args:
			amount: Amount to spend.

		Raises:
			ValueError: If amount exceeds available budget.
		"""
		if amount > self._budget:
			raise ValueError("Insufficient budget for this expense")
		self._budget -= amount

	def donate(self, amount: float) -> float:
		"""Donate part of the visitor budget and return donated amount.

		Args:
			amount: Amount to donate.

		Returns:
			The amount donated.

		Raises:
			ValueError: If amount exceeds available budget.
		"""
		if amount > self._budget:
			raise ValueError("Insufficient budget for this donation")
		self._budget -= amount
		return amount

	def get_status(self) -> str:
		"""Return a summary of the visitor state.

		Returns:
			A formatted status string.
		"""
		return (
			f"{self.__name} - satisfaction: {self._satisfaction:.1f}, "
			f"budget: ${self._budget:.2f}, "
			f"visited enclosures: {len(self._visited_enclosures)}"
		)

	def __str__(self) -> str:
		"""Return a human-readable visitor string.

		Returns:
			A formatted visitor summary string.
		"""
		return (
			f"Visitor {self.__visitor_id} ({self.__name}) — "
			f"satisfaction: {self._satisfaction:.1f}, "
			f"budget: ${self._budget:.2f}"
		)
