from dataclasses import dataclass
from typing import Dict, Union, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Информация о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIE_1: int = 18
    CALORIE_2: int = 20
    MIN_IN_H: int = 60

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: бег."""

        run_1 = self.CALORIE_1 * self.get_mean_speed() - self.CALORIE_2

        return (run_1 * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALK_1: float = 0.035
    WALK_2: float = 0.029
    MIN_IN_H: int = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: спортивная ходьба."""

        s_walk_1 = ((self.get_mean_speed()**2 // self.height)
                    * self.WALK_2 * self.weight)
        s_walk_2 = self.WALK_1 * self.weight + s_walk_1

        return s_walk_2 * self.duration * self.MIN_IN_H


class Swimming(Training):
    """Тренировка: плавание."""

    SWM_1: float = 1.1
    SWM_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return self.length_pool * self.count_pool \
            / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий при плавании."""
        return (self.get_mean_speed() + self.SWM_1) * self.SWM_2 * self.weight

    def get_distance(self) -> float:
        """Получить дистанцию в км. при плавании."""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""

    train_dict: Dict[str, Type(Training)] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    return train_dict[workout_type](*data)


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
