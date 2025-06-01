"""
Домашнє завдання #10: Лінійне програмування та рандомізовані алгоритми
Завдання 1: Оптимізація виробництва напоїв

Задача: Максимізувати виробництво "Лимонаду" та "Фруктового соку"
при обмежених ресурсах, використовуючи лінійне програмування (PuLP).
"""

import pulp
from typing import Dict, Tuple

def solve_production_optimization():
    """
    Розв'язує задачу оптимізації виробництва напоїв.
    
    Returns:
        Tuple: (статус_розв'язання, кількість_лимонаду, кількість_фруктового_соку, загальна_кількість)
    """
    
    # Створюємо модель лінійного програмування (максимізація)
    model = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)
    
    # Змінні рішення (кількість продуктів для виробництва)
    # x1 - кількість одиниць "Лимонаду"
    # x2 - кількість одиниць "Фруктового соку"
    lemonade = pulp.LpVariable("Lemonade", lowBound=0, cat='Integer')
    fruit_juice = pulp.LpVariable("Fruit_Juice", lowBound=0, cat='Integer')
    
    # Цільова функція: максимізувати загальну кількість продуктів
    model += lemonade + fruit_juice, "Total_Products"
    
    # Обмеження ресурсів:
    
    # 1. Вода: Лимонад потребує 2 од., Фруктовий сік потребує 1 од., всього доступно 100 од.
    model += 2 * lemonade + 1 * fruit_juice <= 100, "Water_Constraint"
    
    # 2. Цукор: тільки для Лимонаду потрібна 1 од., всього доступно 50 од.
    model += 1 * lemonade <= 50, "Sugar_Constraint"
    
    # 3. Лимонний сік: тільки для Лимонаду потрібна 1 од., всього доступно 30 од.
    model += 1 * lemonade <= 30, "Lemon_Juice_Constraint"
    
    # 4. Фруктове пюре: тільки для Фруктового соку потрібно 2 од., всього доступно 40 од.
    model += 2 * fruit_juice <= 40, "Fruit_Puree_Constraint"
    
    # Розв'язуємо задачу
    model.solve()
    
    # Отримуємо результати
    status = pulp.LpStatus[model.status]
    lemonade_qty = int(lemonade.varValue) if lemonade.varValue else 0
    fruit_juice_qty = int(fruit_juice.varValue) if fruit_juice.varValue else 0
    total_products = lemonade_qty + fruit_juice_qty
    
    return status, lemonade_qty, fruit_juice_qty, total_products, model

def analyze_resource_usage(lemonade_qty: int, fruit_juice_qty: int):
    """
    Аналізує використання ресурсів при заданому виробництві.
    
    Args:
        lemonade_qty: Кількість лимонаду
        fruit_juice_qty: Кількість фруктового соку
        
    Returns:
        Dict: Інформація про використання ресурсів
    """
    
    # Розрахунок використання ресурсів
    resources = {
        "Вода": {
            "використано": 2 * lemonade_qty + 1 * fruit_juice_qty,
            "доступно": 100,
            "залишок": 100 - (2 * lemonade_qty + 1 * fruit_juice_qty)
        },
        "Цукор": {
            "використано": 1 * lemonade_qty,
            "доступно": 50,
            "залишок": 50 - (1 * lemonade_qty)
        },
        "Лимонний сік": {
            "використано": 1 * lemonade_qty,
            "доступно": 30,
            "залишок": 30 - (1 * lemonade_qty)
        },
        "Фруктове пюре": {
            "використано": 2 * fruit_juice_qty,
            "доступно": 40,
            "залишок": 40 - (2 * fruit_juice_qty)
        }
    }
    
    return resources

def display_results(status: str, lemonade_qty: int, fruit_juice_qty: int, 
                   total_products: int, resources: Dict):
    """
    Відображає результати оптимізації.
    """
    print("🏭 РЕЗУЛЬТАТИ ОПТИМІЗАЦІЇ ВИРОБНИЦТВА НАПОЇВ")
    print("=" * 60)
    
    print(f"\n📊 Статус розв'язання: {status}")
    
    if status == "Optimal":
        print(f"\n🎯 Оптимальне рішення:")
        print(f"   • Лимонад: {lemonade_qty} одиниць")
        print(f"   • Фруктовий сік: {fruit_juice_qty} одиниць")
        print(f"   • Загальна кількість продуктів: {total_products} одиниць")
        
        print(f"\n📈 Використання ресурсів:")
        for resource, data in resources.items():
            usage_percent = (data['використано'] / data['доступно']) * 100
            status_emoji = "🔴" if data['залишок'] == 0 else "🟡" if usage_percent > 80 else "🟢"
            
            print(f"   {status_emoji} {resource}:")
            print(f"      Використано: {data['використано']}/{data['доступно']} "
                  f"({usage_percent:.1f}%)")
            print(f"      Залишок: {data['залишок']} одиниць")
        
        # Визначення лімітуючих ресурсів
        limiting_resources = [name for name, data in resources.items() 
                            if data['залишок'] == 0]
        
        if limiting_resources:
            print(f"\n⚠️  Лімітуючі ресурси: {', '.join(limiting_resources)}")
        else:
            print(f"\n✅ Всі ресурси мають залишки")
            
    else:
        print(f"❌ Не вдалося знайти оптимальне рішення. Статус: {status}")

def sensitivity_analysis():
    """
    Проводить аналіз чутливості - як зміна ресурсів впливає на результат.
    """
    print(f"\n🔍 АНАЛІЗ ЧУТЛИВОСТІ")
    print("=" * 40)
    
    base_status, base_lemonade, base_fruit_juice, base_total, _ = solve_production_optimization()
    
    print(f"Базове рішення: {base_lemonade} лимонаду + {base_fruit_juice} фруктового соку = {base_total} всього")
    
    # Тестуємо збільшення кожного ресурсу на 10%
    scenarios = [
        ("Вода +10%", {"water": 110}),
        ("Цукор +10%", {"sugar": 55}),
        ("Лимонний сік +10%", {"lemon": 33}),
        ("Фруктове пюре +10%", {"puree": 44})
    ]
    
    print(f"\nВплив збільшення ресурсів на 10%:")
    
    for scenario_name, changes in scenarios:
        # Створюємо нову модель з модифікованими ресурсами
        model = pulp.LpProblem("Sensitivity_Test", pulp.LpMaximize)
        
        lemonade = pulp.LpVariable("Lemonade", lowBound=0, cat='Integer')
        fruit_juice = pulp.LpVariable("Fruit_Juice", lowBound=0, cat='Integer')
        
        model += lemonade + fruit_juice, "Total_Products"
        
        # Застосовуємо базові або модифіковані обмеження
        water_limit = changes.get("water", 100)
        sugar_limit = changes.get("sugar", 50)
        lemon_limit = changes.get("lemon", 30)
        puree_limit = changes.get("puree", 40)
        
        model += 2 * lemonade + 1 * fruit_juice <= water_limit, "Water"
        model += 1 * lemonade <= sugar_limit, "Sugar"
        model += 1 * lemonade <= lemon_limit, "Lemon"
        model += 2 * fruit_juice <= puree_limit, "Puree"
        
        model.solve()
        
        if model.status == 1:  # Optimal
            new_lemonade = int(lemonade.varValue) if lemonade.varValue else 0
            new_fruit_juice = int(fruit_juice.varValue) if fruit_juice.varValue else 0
            new_total = new_lemonade + new_fruit_juice
            improvement = new_total - base_total
            
            print(f"   {scenario_name}: {new_total} всього (зміна: {improvement:+d})")

def alternative_objective_functions():
    """
    Тестує альтернативні цільові функції.
    """
    print(f"\n🎯 АЛЬТЕРНАТИВНІ ЦІЛЬОВІ ФУНКЦІЇ")
    print("=" * 45)
    
    # Сценарій 1: Максимізувати прибуток (припустимо різну рентабельність)
    print("1. Максимізація прибутку (Лимонад: 3 грн, Фруктовий сік: 2 грн за одиницю):")
    
    model = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)
    lemonade = pulp.LpVariable("Lemonade", lowBound=0, cat='Integer')
    fruit_juice = pulp.LpVariable("Fruit_Juice", lowBound=0, cat='Integer')
    
    # Цільова функція: максимізувати прибуток
    model += 3 * lemonade + 2 * fruit_juice, "Total_Profit"
    
    # Ті ж обмеження
    model += 2 * lemonade + 1 * fruit_juice <= 100, "Water"
    model += 1 * lemonade <= 50, "Sugar"
    model += 1 * lemonade <= 30, "Lemon"
    model += 2 * fruit_juice <= 40, "Puree"
    
    model.solve()
    
    if model.status == 1:
        profit_lemonade = int(lemonade.varValue) if lemonade.varValue else 0
        profit_fruit_juice = int(fruit_juice.varValue) if fruit_juice.varValue else 0
        total_profit = 3 * profit_lemonade + 2 * profit_fruit_juice
        
        print(f"   Оптимальне рішення: {profit_lemonade} лимонаду + {profit_fruit_juice} фруктового соку")
        print(f"   Загальний прибуток: {total_profit} грн")

def main():
    """
    Головна функція для розв'язання задачі оптимізації виробництва.
    """
    print("💼 ДОМАШНЄ ЗАВДАННЯ #10: ОПТИМІЗАЦІЯ ВИРОБНИЦТВА")
    print("Завдання 1: Лінійне програмування з PuLP")
    print("=" * 65)
    
    print("\n📋 Умови задачі:")
    print("• Продукти: Лимонад, Фруктовий сік")
    print("• Ресурси: Вода (100), Цукор (50), Лимонний сік (30), Фруктове пюре (40)")
    print("• Рецепт Лимонаду: 2 води + 1 цукор + 1 лимонний сік")
    print("• Рецепт Фруктового соку: 1 вода + 2 фруктове пюре")
    print("• Мета: Максимізувати загальну кількість продуктів")
    
    # Розв'язуємо основну задачу
    status, lemonade_qty, fruit_juice_qty, total_products, model = solve_production_optimization()
    
    # Аналізуємо використання ресурсів
    resources = analyze_resource_usage(lemonade_qty, fruit_juice_qty)
    
    # Відображаємо результати
    display_results(status, lemonade_qty, fruit_juice_qty, total_products, resources)
    
    # Додаткові аналізи
    sensitivity_analysis()
    alternative_objective_functions()
    
    print(f"\n💡 ВИСНОВКИ:")
    if status == "Optimal":
        print(f"✅ Знайдено оптимальне рішення:")
        print(f"   • Максимальна кількість продуктів: {total_products}")
        print(f"   • Оптимальний план: {lemonade_qty} лимонаду + {fruit_juice_qty} фруктового соку")
        
        # Визначення найбільш цінних ресурсів
        limiting = [name for name, data in resources.items() if data['залишок'] == 0]
        if limiting:
            print(f"   • Найбільш цінні ресурси: {', '.join(limiting)}")
            print(f"   • Для збільшення виробництва слід збільшити запаси цих ресурсів")
    
    print(f"\n🎉 Завдання 1 виконано успішно!")
    
    return {
        'status': status,
        'lemonade': lemonade_qty,
        'fruit_juice': fruit_juice_qty,
        'total': total_products,
        'resources': resources
    }

if __name__ == "__main__":
    result = main()
