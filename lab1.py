import sys

# Програма для аналізу температурних показів за день

print("=== Аналіз температурних показів за день ===")
print("Введіть до 24 значень температур (через пробіл):")

# Введення температур користувачем
raw_temp_input = input("Температури: ").strip()
temp_tokens = raw_temp_input.split()

# Перевірка кількості значень
if len(temp_tokens) == 0:
    print("Помилка: рядок введення порожній.")
    sys.exit()

if len(temp_tokens) > 24:
    print(f"Помилка: введено {len(temp_tokens)} значень. Допустима кількість — не більше 24.")
    sys.exit()

# Створення та наповнення списку для числових значень показів температур
temperatures = []
for token in temp_tokens:
    try:
        val = float(token)
    except ValueError:
        print(f"Помилка: значення '{token}' не є коректним числом.")
        sys.exit()

    if not (-40.0 <= val <= 40.0):
        print(f"Помилка: температура {val}°C виходить за межі діапазону [-40..40]°C.")
        sys.exit()

    temperatures.append(val)

# Перевірка, чи додались у список хоч якісь дані (список містить значення), інакше завершити програму
if len(temperatures) < 2:
    print("Помилка: для проведення аналізу необхідно ввести щонайменше 2 температурні показники.")
    sys.exit()

# Введення часових міток
print("\nВведіть часові мітки для кожного показу (у форматі 'година:хвилина') через пробіл:")
raw_time_input = input("Мітки часу: ").strip()
time_tokens = raw_time_input.split()

# Перевірка формату часу
valid_times = []
for t in time_tokens:
    parts = t.split(":")
    if len(parts) != 2:
        print(f"Помилка: мітка часу '{t}' не відповідає формату 'година:хвилина' (HH:MM).")
        sys.exit()

    hour_str, min_str = parts[0], parts[1]
    if not (hour_str.isdigit() and min_str.isdigit()):
        print(f"Помилка: мітка часу '{t}' містить нецифрові символи.")
        sys.exit()

    hour, minute = int(hour_str), int(min_str)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        print(f"Помилка: у мітці '{t}' значення годин (0-23) або хвилин (0-59) поза межами.")
        sys.exit()

    valid_times.append(f"{hour:02d}:{minute:02d}")

# Перевірка кількості міток
if len(valid_times) != len(temperatures):
    print(f"Помилка: кількість міток часу ({len(valid_times)}) не збігається з кількістю температур ({len(temperatures)}).")
    sys.exit()

# Створення словника {час: температура, час: температура, ...}
temp_dict = dict(zip(valid_times, temperatures))

# === Обчислення характеристик через словник з даними ===
time_keys = list(temp_dict.keys())
temp_values = list(temp_dict.values())

avg_temp = sum(temp_values) / len(temp_values)
max_temp = max(temp_values)
min_temp = min(temp_values)

positive_count = sum(1 for val in temp_values if val > 0)
negative_count = sum(1 for val in temp_values if val < 0)

sharp_changes = []
for i in range(len(temp_values) - 1):
    diff = abs(temp_values[i + 1] - temp_values[i])
    if diff > 7.0:
        sharp_changes.append((time_keys[i], time_keys[i + 1], diff))

# === Виведення результатів ===
print("\n=== РЕЗУЛЬТАТ АНАЛІЗУ ===")
print("Температурні дані (час → температура):")
for time_mark, val in temp_dict.items():
    print(f"   {time_mark} → {val:6.1f} °C")

print(f"\nЗагальна кількість вимірювань: {len(temp_dict)}")
print(f"Середня температура: {avg_temp:.2f} °C")
print(f"Максимальна температура: {max_temp:.1f} °C")
print(f"Мінімальна температура: {min_temp:.1f} °C")
print(f"Кількість додатних температур: {positive_count}")
print(f"Кількість від’ємних температур: {negative_count}")

# Виведення різких змін
if sharp_changes:
    print("\n[!] Виявлено різкі зміни температури (> 7°):")
    for t1, t2, diff in sharp_changes:
        print(f"  між {t1} та {t2}: зміна на {diff:.1f}°C")
else:
    print("\nРізких змін температури (> 7°) не зафіксовано.")

print("\n=== Кінець аналізу ===")