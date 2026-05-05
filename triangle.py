import math
import logging
from datetime import datetime
from typing import Tuple, List

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('triangle_log.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def calculate_triangle(str_a: str, str_b: str, str_c: str) -> Tuple[str, List[Tuple[int, int]]]:
    """
    Вычисляет вид треугольника и координаты его вершин.
    
    Args:
        str_a: строка, представляющая длину стороны А
        str_b: строка, представляющая длину стороны Б
        str_c: строка, представляющая длину стороны С
    
    Returns:
        Кортеж (тип_треугольника, координаты_вершин)
    """
    
    try:
        # Валидация: попытка преобразовать в float
        a = float(str_a)
        b = float(str_b)
        c = float(str_c)
        
        # Проверка на положительность
        if a <= 0 or b <= 0 or c <= 0:
            logging.warning(f"Отрицательные или нулевые значения: A={a}, B={b}, C={c}")
            return "", [(-1, -1), (-1, -1), (-1, -1)]
        
        # Проверка неравенства треугольника
        if not (a + b > c and b + c > a and a + c > b):
            logging.warning(f"Не треугольник: A={a}, B={b}, C={c}")
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]
        
        # Определение типа треугольника
        eps = 1e-9
        if abs(a - b) < eps and abs(b - c) < eps:
            triangle_type = "равносторонний"
        elif abs(a - b) < eps or abs(b - c) < eps or abs(a - c) < eps:
            triangle_type = "равнобедренный"
        else:
            triangle_type = "разносторонний"
        
        # Вычисление координат вершин
        coordinates = calculate_coordinates(a, b, c)
        
        # Логирование успешного запроса
        logging.info(f"SUCCESS | A={a}, B={b}, C={c} | Type={triangle_type} | Coords={coordinates}")
        
        return triangle_type, coordinates
    
    except ValueError:
        # Нечисловые данные
        logging.error(f"INVALID INPUT | A={str_a}, B={str_b}, C={str_c} | Ошибка: невалидные числовые данные")
        return "", [(-2, -2), (-2, -2), (-2, -2)]
    except Exception as e:
        # Все остальные ошибки
        logging.error(f"ERROR | A={str_a}, B={str_b}, C={str_c} | Exception: {str(e)}", exc_info=True)
        return "", [(-2, -2), (-2, -2), (-2, -2)]


def calculate_coordinates(a: float, b: float, c: float) -> List[Tuple[int, int]]:
    """
    Вычисляет координаты вершин треугольника и масштабирует их для поля 100x100 px.
    
    Вершина A находится в начале координат (0, 0)
    Вершина B находится на оси X на расстоянии c
    Вершина C вычисляется через формулу косинуса
    """
    
    # Вершина A в начале координат
    vertex_a = (0, 0)
    
    # Вершина B на оси X на расстоянии c
    vertex_b = (c, 0)
    
    # Вершина C вычисляется через закон косинусов
    # cos(A) = (b² + c² - a²) / (2bc)
    cos_a = (b**2 + c**2 - a**2) / (2 * b * c)
    sin_a = math.sqrt(1 - cos_a**2)
    
    vertex_c = (b * cos_a, b * sin_a)
    
    # Масштабирование для поля 100x100 px
    vertices = [vertex_a, vertex_b, vertex_c]
    
    # Поиск границ
    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)
    
    # Если все точки совпадают (вырожденный случай)
    if max_x == min_x or max_y == min_y:
        return [(-1, -1), (-1, -1), (-1, -1)]
    
    # Масштабирование с отступом
    scale_x = 90 / (max_x - min_x)
    scale_y = 90 / (max_y - min_y)
    scale = min(scale_x, scale_y)
    
    scaled_vertices = []
    for vx, vy in vertices:
        scaled_x = int((vx - min_x) * scale + 5)
        scaled_y = int((vy - min_y) * scale + 5)
        scaled_vertices.append((scaled_x, scaled_y))
    
    return scaled_vertices


# Тестирование
if __name__ == "__main__":
    print("=== ТЕСТИРОВАНИЕ ФУНКЦИИ ===\n")
    
    # Тест 1: Равносторонний треугольник
    print("Тест 1: Равносторонний треугольник")
    t_type, coords = calculate_triangle("5", "5", "5")
    print(f"Тип: {t_type}, Координаты: {coords}\n")
    
    # Тест 2: Равнобедренный треугольник
    print("Тест 2: Равнобедренный треугольник")
    t_type, coords = calculate_triangle("5", "5", "6")
    print(f"Тип: {t_type}, Координаты: {coords}\n")
    
    # Тест 3: Разносторонний треугольник
    print("Тест 3: Разносторонний треугольник")
    t_type, coords = calculate_triangle("3", "4", "5")
    print(f"Тип: {t_type}, Координаты: {coords}\n")
    
    # Тест 4: Не треугольник
    print("Тест 4: Не треугольник")
    t_type, coords = calculate_triangle("1", "2", "10")
    print(f"Тип: {t_type}, Координаты: {coords}\n")
    
    # Тест 5: Отрицательное значение
    print("Тест 5: Отрицательное значение")
    t_type, coords = calculate_triangle("-5", "5", "5")
    print(f"Тип: {t_type}, Координаты: {coords}\n")
    
    # Тест 6: Невалидные данные
    print("Тест 6: Невалидные данные")
    t_type, coords = calculate_triangle("abc", "5", "5")
    print(f"Тип: {t_type}, Координаты: {coords}\n")