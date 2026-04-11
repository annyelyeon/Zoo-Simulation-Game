class InsufficientFundsError(Exception):
	"""Raised when a purchase exceeds available funds."""


class ResourceManager:
	"""Singleton manager for zoo financial resources and transaction tracking."""

	_instance: "ResourceManager | None" = None
	_initialized: bool = False

	def __new__(cls) -> "ResourceManager":
		"""Create the singleton instance if it does not already exist.

		Returns:
			The singleton ResourceManager instance.
		"""
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self) -> None:
		"""Initialize singleton state only on first creation."""
		if self.__class__._initialized:
			return

		self._funds: float = 500.0
		self._day_expenses: float = 0.0
		self._day_income: float = 0.0
		self._transaction_log: list[str] = []
		self.__class__._initialized = True

	@property
	def funds(self) -> float:
		"""float: Return current available funds."""
		return self._funds

	@property
	def day_expenses(self) -> float:
		"""float: Return total expenses for the current day."""
		return self._day_expenses

	@property
	def day_income(self) -> float:
		"""float: Return total income for the current day."""
		return self._day_income

	@classmethod
	def get_instance(cls) -> "ResourceManager":
		"""Return the singleton ResourceManager instance.

		Returns:
			The singleton ResourceManager instance.
		"""
		return cls()

	def spend(self, amount: float, description: str) -> None:
		"""Record an expense transaction.

		Args:
			amount: Expense amount.
			description: Expense description.

		Raises:
			InsufficientFundsError: If amount exceeds available funds.
		"""
		if amount > self._funds:
			raise InsufficientFundsError("Insufficient funds for this purchase")

		self._funds -= amount
		self._day_expenses += amount
		self._transaction_log.append(f"[EXPENSE] {description}: -${amount:.2f}")

	def earn(self, amount: float, description: str) -> None:
		"""Record an income transaction.

		Args:
			amount: Income amount.
			description: Income description.
		"""
		self._funds += amount
		self._day_income += amount
		self._transaction_log.append(f"[INCOME] {description}: +${amount:.2f}")

	def reset_daily_totals(self) -> None:
		"""Reset per-day income and expense totals to zero."""
		self._day_expenses = 0.0
		self._day_income = 0.0

	def get_summary(self) -> str:
		"""Return a formatted financial summary.

		Returns:
			Multi-line summary including current funds and daily totals.
		"""
		return (
			f"Funds: ${self._funds:.2f}\n"
			f"Today income:   +${self._day_income:.2f}\n"
			f"Today expenses: -${self._day_expenses:.2f}"
		)

	def get_transaction_log(self) -> list[str]:
		"""Return the transaction log.

		Returns:
			List of transaction log entries.
		"""
		return self._transaction_log

	def __str__(self) -> str:
		"""Return the same summary string as get_summary().

		Returns:
			Formatted financial summary.
		"""
		return self.get_summary()
