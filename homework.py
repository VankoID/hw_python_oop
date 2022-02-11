# from typing_extensions import Self
# from mypy.dmypy.client import action

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 LEN_STEP: float = 0.65,
                 M_IN_KM: int = 1000) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = LEN_STEP
        self.M_IN_KM = M_IN_KM

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self):
        coeff_calorie_r1 = 18
        coeff_calorie_r2 = 20
        calories = ((coeff_calorie_r1
                    * self.get_mean_speed() - coeff_calorie_r2)
                    * (self.weight / self.M_IN_KM * self.duration)
                    )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action,
                 duration,
                 weight,
                 height,
                 ) -> None:

        super().__init__(action,
                         duration,
                         weight,
                         )

        self.height = height

    def get_spent_calories(self):
        coeff_calorie_s1 = 0.035
        coeff_calorie_s2 = 0.029
        calories = ((coeff_calorie_s1 * self.weight)
                    + (self.get_mean_speed() ** 2 // self.height)
                    * (coeff_calorie_s2 * self.weight)
                    * self.duration
                    )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:

        super().__init__(action,
                         duration,
                         weight,
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool

    LEN_STEP = 1.38
    coeff_calories_sw1 = 1.1
    coeff_calories_sw2 = 2

    def get_spent_calories(self):
        calories = (self.get_mean_speed() + self.coeff_calories_sw1
                    * self.coeff_calories_sw2 * self.weight
                    )
        return calories

    def get_mean_speed(self):
        speed = ((self.length_pool
                  * self.count_pool
                  / self.M_IN_KM / self.duration))
        return speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    active_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return active_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
