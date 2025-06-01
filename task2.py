"""
Домашнє завдання #10: Завдання 2
Основні функції для методу Монте-Карло
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi
import random
from typing import Tuple, List

def f(x):
    """
    Функція для інтегрування: f(x) = x^2
    
    Args:
        x: Значення x (може бути числом або масивом)
        
    Returns:
        Значення функції f(x) = x^2
    """
    return x ** 2

def analytical_integral(a: float, b: float) -> float:
    """
    Аналітичне обчислення інтеграла функції f(x) = x^2.
    
    Інтеграл від x^2 = x^3/3
    
    Args:
        a: Нижня межа інтегрування
        b: Верхня межа інтегрування
        
    Returns:
        Точне значення інтеграла
    """
    return (b**3 / 3) - (a**3 / 3)

def monte_carlo_integration(func, a: float, b: float, n: int) -> Tuple[float, List[float]]:
    """
    Обчислення інтеграла методом Монте-Карло.
    
    Args:
        func: Функція для інтегрування
        a: Нижня межа інтегрування  
        b: Верхня межа інтегрування
        n: Кількість випадкових точок
        
    Returns:
        Tuple[float, List[float]]: (оцінка інтеграла, історія наближень)
    """
    
    # Генеруємо випадкові точки x в інтервалі [a, b]
    random_x = np.random.uniform(a, b, n)
    
    # Обчислюємо значення функції в цих точках
    function_values = func(random_x)
    
    # Оцінка інтеграла: (b-a) * середнє значення функції
    integral_estimate = (b - a) * np.mean(function_values)
    
    # Зберігаємо історію наближень для аналізу збіжності
    history = []
    running_sum = 0
    
    for i in range(n):
        running_sum += function_values[i]
        current_estimate = (b - a) * running_sum / (i + 1)
        history.append(current_estimate)
    
    return integral_estimate, history

def monte_carlo_geometric_method(func, a: float, b: float, n: int) -> Tuple[float, int, int]:
    """
    Геометричний метод Монте-Карло (підрахунок точок під кривою).
    
    Args:
        func: Функція для інтегрування
        a: Нижня межа інтегрування
        b: Верхня межа інтегрування  
        n: Кількість випадкових точок
        
    Returns:
        Tuple[float, int, int]: (оцінка інтеграла, точки під кривою, загальна кількість точок)
    """
    
    # Знаходимо максимальне значення функції на інтервалі для визначення прямокутника
    x_range = np.linspace(a, b, 1000)
    y_max = np.max(func(x_range))
    
    points_under_curve = 0
    total_points = n
    
    # Генеруємо випадкові точки в прямокутнику [a, b] × [0, y_max]
    for _ in range(n):
        x = random.uniform(a, b)
        y = random.uniform(0, y_max)
        
        # Перевіряємо, чи точка знаходиться під кривою
        if y <= func(x):
            points_under_curve += 1
    
    # Площа під кривою = (площа прямокутника) × (частка точок під кривою)
    rectangle_area = (b - a) * y_max
    integral_estimate = rectangle_area * (points_under_curve / total_points)
    
    return integral_estimate, points_under_curve, total_points

def plot_function_and_integration(a: float, b: float):
    """
    Створює графік функції та області інтегрування.
    """
    # Створення діапазону значень для x
    x = np.linspace(-0.5, 2.5, 400)
    y = f(x)
    
    # Створення графіка
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Малювання функції
    ax.plot(x, y, 'r', linewidth=2, label='f(x) = x²')
    
    # Заповнення області під кривою
    ix = np.linspace(a, b, 100)
    iy = f(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3, label='Область інтегрування')
    
    # Налаштування графіка
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    
    # Додавання меж інтегрування
    ax.axvline(x=a, color='blue', linestyle='--', alpha=0.7, label=f'x = {a}')
    ax.axvline(x=b, color='blue', linestyle='--', alpha=0.7, label=f'x = {b}')
    
    ax.set_title(f'Графік функції f(x) = x² та область інтегрування від {a} до {b}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_convergence(history: List[float], true_value: float, n_points: int):
    """
    Створює графік збіжності методу Монте-Карло.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    iterations = range(1, len(history) + 1)
    
    # Графік збіжності
    ax1.plot(iterations, history, 'b-', alpha=0.7, label='Наближення Монте-Карло')
    ax1.axhline(y=true_value, color='r', linestyle='--', label=f'Точне значення: {true_value:.6f}')
    ax1.set_xlabel('Кількість точок')
    ax1.set_ylabel('Оцінка інтеграла')
    ax1.set_title('Збіжність методу Монте-Карло')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Графік похибки
    errors = [abs(estimate - true_value) for estimate in history]
    ax2.plot(iterations, errors, 'g-', alpha=0.7)
    ax2.set_xlabel('Кількість точок')
    ax2.set_ylabel('Абсолютна похибка')
    ax2.set_title('Похибка наближення')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("📚 Завантажено функції для методу Монте-Карло")
    print("Запустіть task2_part2.py для виконання обчислень")
def compare_methods(a: float, b: float, n_points: List[int]):
    """
    Порівнює точність методу Монте-Карло для різної кількості точок.
    """
    print(f"\n📊 ПОРІВНЯННЯ ТОЧНОСТІ ДЛЯ РІЗНОЇ КІЛЬКОСТІ ТОЧОК")
    print("=" * 65)
    
    true_value = analytical_integral(a, b)
    scipy_result, scipy_error = spi.quad(f, a, b)
    
    print(f"Аналітичне значення: {true_value:.8f}")
    print(f"SciPy quad результат: {scipy_result:.8f} ± {scipy_error:.2e}")
    print()
    
    print(f"{'Точки':<8} {'Монте-Карло':<12} {'Похибка':<12} {'Відн. похибка (%)':<18}")
    print("-" * 65)
    
    for n in n_points:
        mc_result, _ = monte_carlo_integration(f, a, b, n)
        error = abs(mc_result - true_value)
        relative_error = (error / true_value) * 100
        
        print(f"{n:<8} {mc_result:<12.6f} {error:<12.6f} {relative_error:<18.4f}")

def demonstrate_geometric_method(a: float, b: float, n: int):
    """
    Демонструє геометричний метод Монте-Карло з візуалізацією.
    """
    print(f"\n🎯 ГЕОМЕТРИЧНИЙ МЕТОД МОНТЕ-КАРЛО")
    print("=" * 40)
    
    # Виконуємо геометричний метод
    geometric_result, points_under, total_points = monte_carlo_geometric_method(f, a, b, n)
    
    print(f"Кількість точок: {total_points}")
    print(f"Точки під кривою: {points_under}")
    print(f"Частка точок під кривою: {points_under/total_points:.4f}")
    print(f"Оцінка інтеграла: {geometric_result:.6f}")
    
    # Візуалізація геометричного методу
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Малюємо функцію
    x_plot = np.linspace(a, b, 100)
    y_plot = f(x_plot)
    ax.plot(x_plot, y_plot, 'r-', linewidth=2, label='f(x) = x²')
    
    # Генеруємо точки для візуалізації (менше для читабельності)
    vis_n = min(500, n)
    x_range = np.linspace(a, b, 1000)
    y_max = np.max(f(x_range))
    
    x_points = np.random.uniform(a, b, vis_n)
    y_points = np.random.uniform(0, y_max, vis_n)
    
    # Розфарбовуємо точки
    colors = ['green' if y <= f(x) else 'red' for x, y in zip(x_points, y_points)]
    ax.scatter(x_points, y_points, c=colors, alpha=0.6, s=1)
    
    ax.set_xlim([a, b])
    ax.set_ylim([0, y_max])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Геометричний метод Монте-Карло\nЗелені точки під кривою, червоні - над нею')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def main():
    """
    Головна функція для виконання завдання з інтеграла.
    """
    print("🎲 ДОМАШНЄ ЗАВДАННЯ #10: МЕТОД МОНТЕ-КАРЛО")
    print("Завдання 2: Обчислення визначеного інтеграла")
    print("=" * 55)
    
    # Параметри інтегрування
    a, b = 0, 2  # Межі інтегрування
    n = 100000   # Кількість точок для основного обчислення
    
    print(f"\n📋 Параметри:")
    print(f"• Функція: f(x) = x²")
    print(f"• Межі інтегрування: [{a}, {b}]")
    print(f"• Кількість точок Монте-Карло: {n:,}")
    
    # Візуалізація функції та області інтегрування
    print(f"\n📈 Створення графіка функції...")
    plot_function_and_integration(a, b)
    
    # Обчислення точного значення
    true_value = analytical_integral(a, b)
    print(f"\n🎯 Аналітичне обчислення:")
    print(f"∫[{a}→{b}] x² dx = [x³/3][{a}→{b}] = {b}³/3 - {a}³/3 = {true_value:.8f}")
    
    # Перевірка за допомогою SciPy
    scipy_result, scipy_error = spi.quad(f, a, b)
    print(f"\n🔬 Перевірка з SciPy quad:")
    print(f"Результат: {scipy_result:.8f}")
    print(f"Оцінка похибки: {scipy_error:.2e}")
    
    # Обчислення методом Монте-Карло
    print(f"\n🎲 Метод Монте-Карло:")
    mc_result, history = monte_carlo_integration(f, a, b, n)
    mc_error = abs(mc_result - true_value)
    mc_relative_error = (mc_error / true_value) * 100
    
    print(f"Результат: {mc_result:.8f}")
    print(f"Абсолютна похибка: {mc_error:.8f}")
    print(f"Відносна похибка: {mc_relative_error:.4f}%")
    
    # Графік збіжності
    print(f"\n📊 Аналіз збіжності...")
    plot_convergence(history, true_value, n)
    
    # Порівняння для різної кількості точок
    n_points = [100, 1000, 10000, 100000, 1000000]
    compare_methods(a, b, n_points)
    
    # Демонстрація геометричного методу
    demonstrate_geometric_method(a, b, 10000)
    
    # Порівняння результатів
    print(f"\n📋 ПІДСУМКОВЕ ПОРІВНЯННЯ:")
    print("=" * 50)
    print(f"{'Метод':<20} {'Значення':<12} {'Похибка':<12}")
    print("-" * 50)
    print(f"{'Аналітичний':<20} {true_value:<12.8f} {'0.00000000':<12}")
    print(f"{'SciPy quad':<20} {scipy_result:<12.8f} {abs(scipy_result-true_value):<12.8f}")
    print(f"{'Монте-Карло':<20} {mc_result:<12.8f} {mc_error:<12.8f}")
    
    # Висновки
    print(f"\n💡 ВИСНОВКИ:")
    print("=" * 20)
    
    if mc_relative_error < 1:
        accuracy_level = "відмінна"
    elif mc_relative_error < 5:
        accuracy_level = "хороша"
    elif mc_relative_error < 10:
        accuracy_level = "задовільна"
    else:
        accuracy_level = "низька"
    
    print(f"✅ Метод Монте-Карло показав {accuracy_level} точність")
    print(f"✅ Відносна похибка: {mc_relative_error:.4f}%")
    print(f"✅ Метод збігається до точного значення при збільшенні кількості точок")
    print(f"✅ Геометричний підхід дає інтуїтивне розуміння методу")
    
    # Рекомендації
    print(f"\n🎯 РЕКОМЕНДАЦІЇ:")
    print("• Для точності 1%: використовуйте > 100,000 точок")
    print("• Для точності 0.1%: використовуйте > 1,000,000 точок")
    print("• Метод ефективний для багатовимірних інтегралів")
    print("• Збіжність пропорційна 1/√n, де n - кількість точок")
    
    print(f"\n🎉 Завдання 2 виконано успішно!")
    
    return {
        'analytical': true_value,
        'scipy': scipy_result,
        'monte_carlo': mc_result,
        'error': mc_error,
        'relative_error': mc_relative_error
    }

if __name__ == "__main__":
    result = main()
