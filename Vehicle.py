from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# ----------------------------- Engine Class -----------------------------
class Engine:
    def __init__(self, horsepower: int, engine_type: str):
        valid_types = ["2-stroke", "4-stroke", "electric", "diesel"]
        if horsepower <= 0:
            raise ValueError("Horsepower must be positive.")
        if engine_type not in valid_types:
            raise ValueError(f"Invalid engine type. Choose from: {valid_types}")
        self.horsepower = horsepower
        self.engine_type = engine_type

    def __str__(self):
        return f"{self.horsepower} HP {self.engine_type} engine"

# ----------------------------- Base Abstract Class -----------------------------
class Vehicle(ABC):
    def __init__(self, brand: str, model: str, year: int, fuel_type: str):
        self._validate_nonempty(brand, "Brand")
        self._validate_nonempty(model, "Model")
        self._validate_year(year)
        self._validate_fuel(fuel_type)
        self._brand = brand
        self._model = model
        self._year = year
        self._fuel_type = fuel_type
        self.__vin = self._generate_vin()

    @staticmethod
    def _validate_nonempty(value, field):
        if not value:
            raise ValueError(f"{field} cannot be empty.")

    @staticmethod
    def _validate_year(year):
        current_year = datetime.now().year
        if not (1900 <= year <= current_year):
            raise ValueError("Invalid year.")

    @staticmethod
    def _validate_fuel(fuel_type):
        valid = ["petrol", "diesel", "electric"]
        if fuel_type not in valid:
            raise ValueError(f"Invalid fuel type. Choose from: {valid}")

    def _generate_vin(self):
        return str(uuid.uuid4())

    @property
    def vin(self):
        return self.__vin

    @abstractmethod
    def start_engine(self):
        pass

    @abstractmethod
    def vehicle_type(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(brand='{self._brand}', model='{self._model}', year={self._year}, fuel='{self._fuel_type}')"

    def __str__(self):
        return f"{self._year} {self._brand} {self._model} ({self._fuel_type})"

# ----------------------------- Mixin -----------------------------
class vehicleMixin:
    def __init__(self):
        self._speed = 0
        self.__odometer = 0

    def accelerate(self, speed: int):
        if speed <= 0:
            raise ValueError("Speed can't be negative")
        self._speed += speed

    def brake(self):
        self._speed = 0
        return f"{self} stopped."

    def drive(self, distance: float):
        if distance <= 0:
            raise ValueError("Distance must be greater than zero.")
        self.__odometer += distance
        return f"{self} drove {distance} km. Total: {self.__odometer} km"

    @property
    def odometer(self):
        return self.__odometer

    @property
    def speed(self):
        return self._speed

# ----------------------------- Motorcycle Class -----------------------------
class Motorcycle(Vehicle, vehicleMixin):
    def __init__(self, brand: str, model: str, year: int, fuel_type: str, engine: Engine, has_sidecar=False):
        super().__init__(brand, model, year, fuel_type)
        vehicleMixin.__init__(self)
        self._engine = engine
        self._has_sidecar = has_sidecar
        self._helmet_required = True

    def start_engine(self):
        return f"{self} engine started. Engine: {self._engine}"

    def vehicle_type(self):
        return "Motorcycle"

    def ride(self, km: float):
        if km <= 0:
            raise ValueError("Distance must be greater than zero.")
        self.accelerate(60)
        self.drive(km)
        return f"{self} rode {km} km. Total: {self.odometer} km"

    def check_helmet(self):
        return f"Helmet required: {'Yes' if self._helmet_required else 'No'}"

    def attach_sidecar(self):
        if self._has_sidecar:
            return "Sidecar already attached."
        self._has_sidecar = True
        return "Sidecar successfully attached."

    def display_info(self):
        sidecar = "Yes" if self._has_sidecar else "No"
        return (
            f"Vehicle: {self}\n"
            f"Type: {self.vehicle_type()}\n"
            f"Fuel: {self._fuel_type}\n"
            f"Engine: {self._engine}\n"
            f"Sidecar: {sidecar}\n"
            f"Odometer: {self.odometer} km\n"
            f"Speed: {self.speed} km/h\n"
            f"VIN: {self.vin}\n"
        )

# ----------------------------- Bus Class -----------------------------
class Bus(Vehicle, vehicleMixin):
    def __init__(self, brand: str, model: str, year: int, fuel_type: str, color: str, capacity: int, engine: Engine):
        super().__init__(brand, model, year, fuel_type)
        vehicleMixin.__init__(self)
        self._color = color
        self.__capacity = capacity
        self._engine = engine
        self._passengers = []

    def vehicle_type(self):
        return "Bus"

    def start_engine(self):
        return f"{self} engine started. Engine: {self._engine}"

    def stop_engine(self):
        return f"{self} engine stopped at {self.speed} km/h."

    def change_color(self, new_color):
        if new_color != self._color:
            self._color = new_color
            return f"Color changed to {new_color}."
        return "Color is already the same."

    def increase_horse_power(self, hp):
        if hp > 0:
            self._engine.horsepower += hp
            return f"Horsepower increased to {self._engine.horsepower}."
        return "Invalid horsepower increment."

    def add_passenger(self, name):
        if len(self._passengers) < self.__capacity:
            self._passengers.append(name)
            return f"{name} ავიდა ავტობუსში"
        return "ავტობუსი სავსეა!"

    def remove_passenger(self, name):
        if name in self._passengers:
            self._passengers.remove(name)
            return f"{name} ჩამოვიდა ავტობუსიდან"
        return f"{name} არ არის ამ ავტობუსში"

    def display_info(self):
        passengers_list = ", ".join(self._passengers) if self._passengers else "No passengers"
        return (
            f"Vehicle: {self}\n"
            f"Type: {self.vehicle_type()}\n"
            f"Color: {self._color}\n"
            f"Engine: {self._engine}\n"
            f"Capacity: {self.__capacity}\n"
            f"Passengers: {len(self._passengers)} / {self.__capacity}\n"
            f"Passenger List: {passengers_list}\n"
            f"Odometer: {self.odometer} km\n"
            f"Speed: {self.speed} km/h\n"
            f"VIN: {self.vin}\n"
        )

# ----------------------------- Car Class -----------------------------
class Car(Vehicle, vehicleMixin):
    model_produced = 0

    def __init__(self, brand: str, model: str, year: int, fuel_type: str, engine: Engine,
                 color: str, num_doors: int, license_plate: str):
        super().__init__(brand, model, year, fuel_type)
        vehicleMixin.__init__(self)
        self._engine = engine
        self._color = color
        self._num_doors = num_doors
        self.__license_plate = license_plate
        self.__class__.model_produced += 1

    @property
    def license_plate(self):
        return self.__license_plate

    @license_plate.setter
    def license_plate(self, new: str):
        self.__license_plate = new

    def start_engine(self):
        return f"{self} engine started. Engine: {self._engine}"

    def vehicle_type(self):
        return "Car"

    def display_info(self):
        return (
            f"Vehicle: {self}\n"
            f"Type: {self.vehicle_type()}\n"
            f"Fuel: {self._fuel_type}\n"
            f"Engine: {self._engine}\n"
            f"Color: {self._color}\n"
            f"Doors: {self._num_doors}\n"
            f"License Plate: {self.__license_plate}\n"
            f"Odometer: {self.odometer} km\n"
            f"Speed: {self.speed} km/h\n"
            f"VIN: {self.vin}\n"
        )

# ----------------------------- SportsCar Class -----------------------------
class SportsCar(Car):
    spoiler_types = {"lip", "wing", "active"}

    def __init__(self, brand: str, model: str, year: int, fuel_type: str, engine: Engine,
                 color: str, num_doors: int, license_plate: str):
        super().__init__(brand, model, year, fuel_type, engine, color, num_doors, license_plate)
        self.__turbo_enabled = False
        self._gear = 1
        self._spoiler = None

    def vehicle_type(self):
        return "Sports Car"

    def enable_turbo(self):
        self.__turbo_enabled = True
        print("Turbo mode is activated.")

    def disable_turbo(self):
        self.__turbo_enabled = False
        print("Turbo mode deactivated.")

    def shift_gear(self, gear: int):
        if gear < 1 or gear > 6:
            raise ValueError("Gear must be between 1 and 6.")
        self._gear = gear
        print(f"Gear shifted to {self._gear}")

    @property
    def spoiler(self):
        return self._spoiler

    def set_spoiler(self, spoiler: str):
        if spoiler not in self.spoiler_types:
            raise ValueError(f"Invalid spoiler. Choose from: {self.spoiler_types}")
        self._spoiler = spoiler
        print(f"Spoiler set to: {spoiler}")

    def display_info(self):
        base = super().display_info()
        return base + (
            f"Turbo: {'Enabled' if self.__turbo_enabled else 'Disabled'}\n"
            f"Gear: {self._gear}\n"
            f"Spoiler: {self._spoiler if self._spoiler else 'None'}\n"
        )

# ----------------------------- Runtime Tests -----------------------------
def main():
    try:
        # Motorcycle tests
        engine1 = Engine(120, "4-stroke")
        moto1 = Motorcycle("Yamaha", "MT-09", 2023, "petrol", engine1)

        engine2 = Engine(100, "4-stroke")
        moto2 = Motorcycle("Royal Enfield", "Classic 500", 2021, "diesel", engine2)

        engine3 = Engine(85, "electric")
        moto3 = Motorcycle("Zero", "SR/F", 2024, "electric", engine3)


        for m in [moto1, moto2, moto3]:
            print(m.display_info())
            print(m.start_engine())
            if m._brand == "Yamaha":
                print(m.ride(100))
            elif m._brand == "Royal Enfield":
                print(m.ride(50))
            elif m._brand == "Zero":
                print(m.ride(25))
            if m._brand != "Zero":
                print(m.attach_sidecar())
            print(m.check_helmet())
            print(f"Current speed: {m.speed} km/h")
            print(m.display_info())
            print("="*40)

        # Bus tests
        bus_engine1 = Engine(280, "4-stroke")
        bus_engine2 = Engine(440, "electric")
        bus_engine3 = Engine(102, "4-stroke")

        bus1 = Bus("MAN", "Lion's City", 2017, "diesel", "Blue", 50, bus_engine1)
        bus2 = Bus("MAN", "Lion's Coach", 2020, "electric", "White", 45, bus_engine2)
        bus3 = Bus("MAN", "TGE Minibus", 2025, "diesel", "Black", 20, bus_engine3)

        for b in [bus1, bus2, bus3]:
            print(b.display_info())
            print(b.start_engine())
            print(b.change_color("Yellow"))
            print(b.increase_horse_power(50))
            print(b.add_passenger("Luka"))
            print(b.add_passenger("Giorgi"))
            print(b.remove_passenger("Luka"))
            print(b.accelerate(40))
            print(b.drive(60))
            print(f"Current speed: {b.speed} km/h")
            print(b.display_info())
            print(b.stop_engine())
            print("="*40)

        # Car tests
        car_engine1 = Engine(150, "4-stroke")
        car1 = Car("BMW", "M3", 2022, "petrol", car_engine1, "Red", 4, "ABC-123")

        car_engine2 = Engine(170, "electric")
        car2 = Car("Tesla", "Model S", 2024, "electric", car_engine2, "White", 4, "EV-001")

        for c in [car1, car2]:
            print(c.display_info())
            print(c.start_engine())
            print(c.accelerate(80))
            print(c.drive(100))
            print(f"Current speed: {c.speed} km/h")
            print(c.brake())
            print(c.display_info())
            print("="*40)


        # SportsCar tests
        sport_engine1 = Engine(320, "4-stroke")
        sport1 = SportsCar("Ferrari", "488 GTB", 2020, "petrol", sport_engine1, "Red", 2, "SPD-488")

        sport_engine2 = Engine(390, "4-stroke")
        sport2 = SportsCar("Lamborghini", "Huracan", 2021, "petrol", sport_engine2, "Green", 2, "LMB-666")

        for s in [sport1, sport2]:
            print(s.display_info())
            print(s.start_engine())
            s.accelerate(120)
            s.drive(150)
            print(f"Current speed: {s.speed} km/h")
            s.enable_turbo()
            s.shift_gear(3)
            s.set_spoiler("wing")
            print(s.display_info())
            s.brake()
            print("="*40)

        sport_engine = Engine(320, "4-stroke")
        sport = SportsCar("Ferrari", "488 GTB", 2020, "petrol", sport_engine, "Red", 2, "SPD-488")

        print(sport.display_info())
        print(sport.start_engine())
        sport.accelerate(120)
        print(sport.drive(150))
        sport.enable_turbo()
        sport.shift_gear(4)
        sport.set_spoiler("wing")
        print(sport.display_info())
        print(sport.brake())
        print("="*40)

        # Summary
        print(f"Total models produced: {Car.model_produced}")

    except ValueError as ve:
        print("❌ Value error:", ve)

    except Exception as e:
        print("❌ Runtime error:", e)

if __name__ == "__main__":
    main()