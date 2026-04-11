from abc import ABC, abstractmethod

from food import Food

class IncompatibleFoodError(Exception):
    """Raised when an animal is fed a food type it cannot eat."""

class Animal(ABC):

    def __init__(self, name, health=100, hunger=0, happiness=50): 
        self.__name = name
        self._health = health
        self._hunger = hunger
        self._happiness = happiness
    
    @property
    def name(self):
        return self.__name
    
    @abstractmethod
    def make_sound(self):
        pass
    
    @abstractmethod
    def eat(self, food_item): # food_item is a string representing the type of food            
        pass
    
    # Update animal status by incrementing hunger and potentially decreasing health.
    def update_status(self):        
        """
        Called once per day to simulate metabolic needs.
        - Hunger increases by 1 (max 100)
        - Health decreases by 1 if hunger is high (max 100)
        """
        # Increase hunger
        if self._hunger < 100:
            self._hunger += 1
        
        # Decrease health if hunger is too high
        if self._hunger > 80 and self._health > 0:
            self._health -= 1
    
    def get_status(self):
        """Return a string representation of the animal's current status."""
        return f"{self.__name} - Health: {self._health}, Hunger: {self._hunger}"


class Mammal(Animal, ABC):
    """Abstract base class for mammals in the zoo simulation."""

    def __init__(
        self,
        name: str,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
        has_fur: bool = True,
        is_nocturnal: bool = False,
    ) -> None:
        """Initialize a mammal with shared animal and mammal-specific attributes.

        Args:
            name: Name of the mammal.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.
            has_fur: Whether the mammal has fur.
            is_nocturnal: Whether the mammal is primarily active at night.
        """
        super().__init__(
            name=name,
            health=health,
            hunger=hunger,
            happiness=happiness,
        )
        self._has_fur = has_fur
        self._is_nocturnal = is_nocturnal

    @abstractmethod
    def groom(self) -> None:
        """Perform species-specific grooming behavior."""
        pass

    def sleep(self) -> None:
        """Put the mammal to sleep and restore a small amount of health.
        Health increases by 5 and is capped at 100.
        """
        print(f"{self.name} is sleeping.")
        self._health = min(100, self._health + 5)


class Marsupial(Mammal, ABC):
    """Abstract base class for marsupials in the zoo simulation."""

    def __init__(
        self,
        name: str,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
        has_fur: bool = True,
        is_nocturnal: bool = False,
        pouch_capacity: int = 1,
    ) -> None:
        """Initialize a marsupial with mammal and pouch-related attributes.

        Args:
            name: Name of the marsupial.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.
            has_fur: Whether the marsupial has fur.
            is_nocturnal: Whether the marsupial is primarily active at night.
            pouch_capacity: Number of young the pouch can carry.

        Raises:
            ValueError: If pouch_capacity is less than 0.
        """
        super().__init__(
            name=name,
            health=health,
            hunger=hunger,
            happiness=happiness,
            has_fur=has_fur,
            is_nocturnal=is_nocturnal,
        )
        self.pouch_capacity = pouch_capacity

    @property
    def pouch_capacity(self) -> int:
        """int: Return the maximum number of young the pouch can hold."""
        return self.__pouch_capacity

    @pouch_capacity.setter
    def pouch_capacity(self, value: int) -> None:
        """Set the pouch capacity.

        Args:
            value: New pouch capacity value.

        Raises:
            ValueError: If value is less than 0.
        """
        if value < 0:
            raise ValueError("pouch_capacity must be >= 0")
        self.__pouch_capacity = value

    @abstractmethod
    def carry_young(self) -> None:
        """Carry young using species-specific pouch behavior."""
        pass

    def sleep(self) -> None:
        """Put the marsupial to sleep in short bursts and restore health.

        Health increases by 3 and is capped at 100.
        Happiness increases by 2 and is capped at 100.
        """
        print(f"{self.name} sleeps in short bursts.")
        self._health = min(100, self._health + 3)
        self._happiness = min(100, self._happiness + 2)


class Kangaroo(Marsupial):
    """Concrete marsupial class representing a kangaroo."""

    def __init__(
        self,
        name: str,
        jump_height: float,
        mob_size: int,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
        has_fur: bool = True,
        is_nocturnal: bool = False,
        pouch_capacity: int = 1,
    ) -> None:
        """Initialize a kangaroo with mobility and social-group attributes.

        Args:
            name: Name of the kangaroo.
            jump_height: Maximum jump height in meters.
            mob_size: Number of kangaroos in the group.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.
            has_fur: Whether the kangaroo has fur.
            is_nocturnal: Whether the kangaroo is primarily active at night.
            pouch_capacity: Number of young the pouch can carry.
        """
        super().__init__(
            name=name,
            health=health,
            hunger=hunger,
            happiness=happiness,
            has_fur=has_fur,
            is_nocturnal=is_nocturnal,
            pouch_capacity=pouch_capacity,
        )
        self._jump_height = jump_height
        self._mob_size = mob_size

    def make_sound(self) -> str:
        """Return the signature sound of a kangaroo.

        Returns:
            The kangaroo sound string.
        """
        return "Thump!"

    def eat(self, food_item: Food) -> None:
        """Feed the kangaroo if the food type is compatible.

        Args:
            food_item: Food object expected to expose a food_type attribute.

        Raises:
            IncompatibleFoodError: If food_item.food_type is not grass or leaves.
        """
        food_type = getattr(food_item, "food_type", None)
        if food_type not in ["grass", "leaves"]:
            raise IncompatibleFoodError(
                f"Kangaroo cannot eat '{food_type}'. Allowed: grass, leaves."
            )
        self._hunger = max(0, self._hunger - food_item.nutritional_value)

    def groom(self) -> None:
        """Groom the kangaroo and increase happiness."""
        print(f"{self.name} grooms its fur carefully.")
        self._happiness += 5

    def carry_young(self) -> None:
        """Carry a joey in the pouch and normalize pouch capacity."""
        print(f"{self.name} carries a joey in its pouch.")
        self.pouch_capacity = 1

    def jump(self) -> None:
        """Print a jump message using the kangaroo's jump height."""
        print(f"{self.name} jumps {self._jump_height:.1f} meters high!")


class Koala(Marsupial):
    """Concrete marsupial class representing a koala."""

    def __init__(
        self,
        name: str,
        eucalyptus_tolerance: float,
        sleep_hours: float = 20.0,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
        has_fur: bool = True,
        is_nocturnal: bool = False,
        pouch_capacity: int = 1,
    ) -> None:
        """Initialize a koala with eucalyptus tolerance and sleep attributes.

        Args:
            name: Name of the koala.
            eucalyptus_tolerance: Tolerance value from 0.0 to 1.0.
            sleep_hours: Typical hours of sleep per day.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.
            has_fur: Whether the koala has fur.
            is_nocturnal: Whether the koala is primarily active at night.
            pouch_capacity: Number of young the pouch can carry.

        Raises:
            ValueError: If eucalyptus_tolerance is outside 0.0 to 1.0.
        """
        if not 0.0 <= eucalyptus_tolerance <= 1.0:
            raise ValueError("eucalyptus_tolerance must be between 0.0 and 1.0")

        super().__init__(
            name=name,
            health=health,
            hunger=hunger,
            happiness=happiness,
            has_fur=has_fur,
            is_nocturnal=is_nocturnal,
            pouch_capacity=pouch_capacity,
        )
        self.__eucalyptus_tolerance = eucalyptus_tolerance
        self._sleep_hours = sleep_hours

    def make_sound(self) -> str:
        """Return the signature sound of a koala.

        Returns:
            The koala sound string.
        """
        return "Bellow!"

    def eat(self, food_item: Food) -> None:
        """Feed the koala if the food type is eucalyptus.

        Args:
            food_item: Food object expected to expose a food_type attribute.

        Raises:
            IncompatibleFoodError: If food_item.food_type is not eucalyptus.
        """
        food_type = getattr(food_item, "food_type", None)
        if food_type != "eucalyptus":
            raise IncompatibleFoodError(
                f"Koala cannot eat '{food_type}'. Allowed: eucalyptus."
            )
        self._hunger = max(0, self._hunger - food_item.nutritional_value)

    def groom(self) -> None:
        """Print a grooming message for the koala."""
        print(f"{self.name} grooms its dense fur while resting in a tree.")

    def carry_young(self) -> None:
        """Print a message about carrying a joey in the pouch."""
        print(f"{self.name} keeps a joey warm in its pouch.")

    def climb(self, tree_name: str) -> None:
        """Print a tree-climbing message.

        Args:
            tree_name: Name of the tree the koala climbs.
        """
        print(f"{self.name} climbs the {tree_name} tree.")

    def deep_sleep(self) -> None:
        """Increase sleep duration and restore a larger amount of health."""
        self._sleep_hours += 2
        self._health = min(100, self._health + 10)


class ISwimmable(ABC):
    """Interface for animals that can swim and dive."""

    @abstractmethod
    def swim(self) -> None:
        """Swim in water."""
        pass

    @abstractmethod
    def dive(self, depth: float) -> None:
        """Dive to a specified depth.

        Args:
            depth: Depth in metres below the water surface.
        """
        pass

class Bird(Animal, ABC):
    """Abstract base class for birds in the zoo simulation."""

    def __init__(
        self,
        name: str,
        wingspan: float,
        feather_colour: str,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
    ) -> None:
        """Initialize a bird with animal and bird-specific attributes.

        Args:
            name: Name of the bird.
            wingspan: Wingspan in centimeters.
            feather_colour: Primary feather color.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.
        """
        super().__init__(
            name=name,
            health=health,
            hunger=hunger,
            happiness=happiness,
        )
        self._wingspan = wingspan
        self._feather_colour = feather_colour

    @abstractmethod
    def make_sound(self) -> str:
        """Produce the species-specific bird sound.

        Returns:
            The sound made by the bird.
        """
        pass

    @abstractmethod
    def eat(self, food_item: Food) -> None:
        """Eat a food item according to bird-specific diet rules.

        Args:
            food_item: Food object consumed by the bird.
        """
        pass

    @abstractmethod
    def preen(self) -> None:
        """Perform feather-maintenance behavior specific to the bird species."""
        pass

    def describe(self) -> None:
        """Print a summary of the bird's wingspan and feather color."""
        print(
            f"{self.name} has a wingspan of {self._wingspan:.1f} cm and "
            f"{self._feather_colour} feathers."
        )


class FlightBird(Bird, ABC):
    """Abstract base class for birds capable of sustained flight."""

    def __init__(
        self,
        name: str,
        wingspan: float,
        feather_colour: str,
        max_altitude: float,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
    ) -> None:
        """Initialize a flight-capable bird.

        Args:
            name: Name of the bird.
            wingspan: Wingspan in centimeters.
            feather_colour: Primary feather color.
            max_altitude: Maximum flight altitude.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.
        """
        super().__init__(
            name=name,
            wingspan=wingspan,
            feather_colour=feather_colour,
            health=health,
            hunger=hunger,
            happiness=happiness,
        )
        self._max_altitude = max_altitude

    @abstractmethod
    def soar(self) -> None:
        """Perform species-specific soaring behavior."""
        pass

    def fly(self) -> None:
        """Print a flight message using the bird's maximum altitude."""
        print(f"{self.name} flies up to {self._max_altitude:.1f} meters.")


class FlightlessBird(Bird, ABC):
    """Abstract base class for birds that do not fly."""

    def __init__(
        self,
        name: str,
        wingspan: float,
        feather_colour: str,
        running_speed: float,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
    ) -> None:
        """Initialize a flightless bird.

        Args:
            name: Name of the bird.
            wingspan: Wingspan in centimeters.
            feather_colour: Primary feather color.
            running_speed: Running speed of the bird.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.
        """
        super().__init__(
            name=name,
            wingspan=wingspan,
            feather_colour=feather_colour,
            health=health,
            hunger=hunger,
            happiness=happiness,
        )
        self._running_speed = running_speed

    @abstractmethod
    def run(self) -> None:
        """Perform species-specific running behavior."""
        pass

    def describe(self) -> None:
        """Print bird details including running speed."""
        super().describe()
        print(f"{self.name} runs at up to {self._running_speed:.1f} km/h.")


class Eagle(FlightBird):
    """Concrete flight bird class representing an eagle."""

    def __init__(
        self,
        name: str,
        wingspan: float,
        feather_colour: str,
        max_altitude: float,
        territory_size: float,
        hunting_skill: float,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
    ) -> None:
        """Initialize an eagle with flight and hunting-related attributes.

        Args:
            name: Name of the eagle.
            wingspan: Wingspan in centimeters.
            feather_colour: Primary feather color.
            max_altitude: Maximum flight altitude.
            territory_size: Territory size used by the eagle.
            hunting_skill: Hunting success tendency in the range 0.0 to 1.0.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.

        Raises:
            ValueError: If hunting_skill is outside 0.0 to 1.0.
        """
        if not 0.0 <= hunting_skill <= 1.0:
            raise ValueError("hunting_skill must be between 0.0 and 1.0")

        super().__init__(
            name=name,
            wingspan=wingspan,
            feather_colour=feather_colour,
            max_altitude=max_altitude,
            health=health,
            hunger=hunger,
            happiness=happiness,
        )
        self.__territory_size = territory_size
        self._hunting_skill = hunting_skill

    def make_sound(self) -> str:
        """Return the eagle's signature sound.

        Returns:
            The eagle sound string.
        """
        return "Screech!"

    def eat(self, food_item: object) -> None:
        """Feed the eagle if the food type is compatible.

        Args:
            food_item: Food object expected to expose a food_type attribute.

        Raises:
            IncompatibleFoodError: If food_item.food_type is not meat.
        """
        food_type = getattr(food_item, "food_type", None)
        if food_type != "meat":
            raise IncompatibleFoodError(
                f"Eagle cannot eat '{food_type}'. Allowed: meat."
            )
        self._hunger = max(0, self._hunger - food_item.nutritional_value)

    def preen(self) -> None:
        """Print a preening message and increase eagle happiness."""
        print(f"{self.name} preens its feathers for smooth flight.")
        self._happiness += 3

    def soar(self) -> None:
        """Print a soaring message using maximum altitude."""
        print(f"{self.name} soars high near {self._max_altitude:.1f} meters.")

    def hunt(self) -> None:
        """Print a hunt result based on hunting skill."""
        if self._hunting_skill > 0.7:
            print(f"{self.name} hunts successfully in its territory.")
        else:
            print(f"{self.name} misses its target during the hunt.")


class Penguin(FlightlessBird, ISwimmable):
    """Concrete flightless bird class representing a penguin."""

    def __init__(
        self,
        name: str,
        wingspan: float,
        feather_colour: str,
        running_speed: float,
        swim_speed: float,
        colony_size: int,
        health: int = 100,
        hunger: int = 0,
        happiness: int = 50,
    ) -> None:
        """Initialize a penguin with running, swimming, and colony attributes.

        Args:
            name: Name of the penguin.
            wingspan: Wingspan in centimeters.
            feather_colour: Primary feather color.
            running_speed: Running speed of the penguin.
            swim_speed: Swimming speed of the penguin.
            colony_size: Number of penguins in the colony.
            health: Initial health value in the range 0-100.
            hunger: Initial hunger value in the range 0-100.
            happiness: Initial happiness value.
        """
        super().__init__(
            name=name,
            wingspan=wingspan,
            feather_colour=feather_colour,
            running_speed=running_speed,
            health=health,
            hunger=hunger,
            happiness=happiness,
        )
        self.__swim_speed = swim_speed
        self._colony_size = colony_size

    def make_sound(self) -> str:
        """Return the penguin's signature sound.

        Returns:
            The penguin sound string.
        """
        return "Squawk!"

    def eat(self, food_item: Food) -> None:
        """Feed the penguin if the food type is fish.

        Args:
            food_item: Food object expected to expose a food_type attribute.

        Raises:
            IncompatibleFoodError: If food_item.food_type is not fish.
        """
        food_type = getattr(food_item, "food_type", None)
        if food_type != "fish":
            raise IncompatibleFoodError(
                f"Penguin cannot eat '{food_type}'. Allowed: fish."
            )
        self._hunger = max(0, self._hunger - food_item.nutritional_value)

    def preen(self) -> None:
        """Print a feather-waterproofing preening message."""
        print(f"{self.name} preens to waterproof its feathers.")

    def run(self) -> None:
        """Print a waddling run message using running speed."""
        print(f"{self.name} waddles at {self._running_speed:.1f} km/h.")

    def swim(self) -> None:
        """Print a swimming message using private swim speed."""
        print(f"{self.name} swims at {self.__swim_speed:.1f} km/h.")

    def dive(self, depth: float) -> None:
            """Print a diving message with the target depth.

            Args:
                depth: Depth in metres below the surface.
            """
            print(f"{self.name} dives to {depth:.1f} metres below the surface.")