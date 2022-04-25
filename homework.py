class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Информация о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    training_type: str = 'Default'
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.distance,
                           self.speed,
                           self.calories)


class Running(Training):
    """Тренировка: бег."""

    training_type: str = 'Running'
    calorie_1: int = 18
    calorie_2: int = 20
    min_60: int = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: бег."""

        return (self.calorie_1 * self.speed - self.calorie_2) \
            * self.weight / self.M_IN_KM * self.duration * self.min_60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    training_type: str = 'SportsWalking'
    walk_1: float = 0.035
    walk_2: float = 0.029
    min_60: int = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        self.height: float = height
        super().__init__(action, duration, weight)
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: спортивная ходьба."""
        return (self.walk_1 * self.weight
                + (self.speed**2 // self.height)
                * self.walk_2 * self.weight) * self.duration * self.min_60


class Swimming(Training):
    """Тренировка: плавание."""

    training_type: str = "Swimming"
    swm_1: float = 1.1
    swm_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        self.count_pool = count_pool
        self.length_pool = length_pool
        super().__init__(action, duration, weight)
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()
        self.distance = self.get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return self.length_pool * self.count_pool \
            / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий при плавании."""
        return (self.speed + self.swm_1) * self.swm_2 * self.weight

    def get_distance(self) -> float:
        """Получить дистанцию в км. при плавании."""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    train_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    return train_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = Training.show_training_info(training)
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
