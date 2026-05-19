#!/usr/bin/env python3
"""
Скрипт для анализа времени выполнения PETSc солвера из лога OpenFOAM
"""

import re
import sys
from collections import defaultdict
import statistics

def parse_log(filename):
    """Парсит лог файл и группирует по решениям"""
    
    solutions = []
    current_solution = None
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Ищем начало решения
        match = re.search(r'before solving (\w+)', line)
        if match:
            var_name = match.group(1)
            if i + 1 < len(lines):
                time_line = lines[i + 1].strip()
                if time_line.isdigit():
                    current_solution = {
                        'variable': var_name,
                        'iteration': 0,  # Будем считать итерации для одной переменной
                        'times': {
                            'start': int(time_line)
                        }
                    }
                    i += 1
                    solutions.append(current_solution)
            i += 1
            continue
        
        # Ищем этапы решения
        if current_solution:
            # Обработка разных этапов
            if 'after creating context' in line:
                match = re.search(r'after creating context (\w+)', line)
                if match and match.group(1) == current_solution['variable']:
                    if i + 1 < len(lines):
                        time_line = lines[i + 1].strip()
                        if time_line.isdigit():
                            current_solution['times']['context'] = int(time_line)
                            i += 1
            
            elif 'after updating Matrix' in line:
                match = re.search(r'after updating Matrix (\w+)', line)
                if match and match.group(1) == current_solution['variable']:
                    if i + 1 < len(lines):
                        time_line = lines[i + 1].strip()
                        if time_line.isdigit():
                            current_solution['times']['matrix_update'] = int(time_line)
                            i += 1
            
            elif 'after solve' in line:
                match = re.search(r'after solve (\w+)', line)
                if match and match.group(1) == current_solution['variable']:
                    if i + 1 < len(lines):
                        time_line = lines[i + 1].strip()
                        if time_line.isdigit():
                            current_solution['times']['solve'] = int(time_line)
                            i += 1
                            
                            # Сбрасываем current_solution для следующего решения
                            current_solution = None
        
        i += 1
    
    # Нумеруем итерации для каждой переменной
    var_counters = defaultdict(int)
    for sol in solutions:
        var_name = sol['variable']
        var_counters[var_name] += 1
        sol['iteration'] = var_counters[var_name]
    
    return solutions

def calculate_durations(solutions):
    """Вычисляет длительности этапов"""
    
    var_stats = defaultdict(lambda: defaultdict(list))
    
    for sol in solutions:
        times = sol['times']
        var_name = sol['variable']
        iteration = sol['iteration']
        
        if 'start' not in times:
            continue
        
        start = times['start']
        durations = {}
        
        # Длительность каждого этапа
        if 'context' in times:
            durations['context'] = times['context'] - start
        
        if 'matrix_update' in times and 'context' in times:
            durations['matrix_update'] = times['matrix_update'] - times['context']
        elif 'matrix_update' in times:
            durations['matrix_update'] = times['matrix_update'] - start
        
        if 'solve' in times and 'matrix_update' in times:
            durations['solve'] = times['solve'] - times['matrix_update']
        elif 'solve' in times and 'context' in times:
            durations['solve'] = times['solve'] - times['context']
        elif 'solve' in times:
            durations['solve'] = times['solve'] - start
        
        if 'solve' in times:
            durations['total'] = times['solve'] - start
        
        # Сохраняем с информацией об итерации
        for stage, duration in durations.items():
            var_stats[var_name][stage].append({
                'duration': duration,
                'iteration': iteration
            })
    
    return var_stats

def format_time(us):
    """Форматирует время в удобные единицы"""
    if us < 1000:
        return f"{us:.0f} мкс"
    elif us < 1000000:
        return f"{us/1000:.2f} мс"
    else:
        return f"{us/1000000:.3f} с"

def print_statistics(var_stats):
    """Выводит статистику"""
    
    print("\n" + "="*90)
    print("СТАТИСТИКА ВРЕМЕНИ ВЫПОЛНЕНИЯ PETSc4Foam")
    print("="*90)
    
    stage_names = {
        'context': 'Создание контекста',
        'matrix_update': 'Обновление матрицы',
        'solve': 'Решение PETSc'
    }
    
    all_stages = defaultdict(list)
    all_totals = []
    
    for var_name, stages in var_stats.items():
        print(f"\n{'─'*90}")
        print(f"Переменная: {var_name}")
        print(f"Всего решений: {len(stages.get('total', []))}")
        print(f"{'─'*90}")
        
        totals = [d['duration'] for d in stages.get('total', [])]
        if not totals:
            continue
        
        avg_total = statistics.mean(totals)
        all_totals.extend(totals)
        
        # Выводим общую информацию
        print(f"\n  Общее время решения:")
        print(f"    Среднее:   {format_time(avg_total):>12}")
        if len(totals) > 1:
            print(f"    Медиана:   {format_time(statistics.median(totals)):>12}")
            print(f"    Диапазон:  {format_time(min(totals)):>5} - {format_time(max(totals)):>10}")
        
        # Выводим каждый этап
        for stage_key, stage_name in stage_names.items():
            stage_data = stages.get(stage_key, [])
            if stage_data:
                times = [d['duration'] for d in stage_data]
                avg_time = statistics.mean(times)
                percentage = (avg_time / avg_total) * 100
                
                print(f"\n  {stage_name}:")
                print(f"    Среднее:   {format_time(avg_time):>12}")
                print(f"    Процент:   {percentage:>11.1f}%")
                if len(times) > 1:
                    print(f"    Медиана:   {format_time(statistics.median(times)):>12}")
                    print(f"    Диапазон:  {format_time(min(times)):>5} - {format_time(max(times)):>10}")
                
                all_stages[stage_key].extend(times)
                
                # Показываем изменение по итерациям
                if len(stage_data) > 1:
                    first = stage_data[0]['duration']
                    last = stage_data[-1]['duration']
                    change = ((last - first) / first) * 100
                    print(f"    Изменение: {change:>+11.1f}% (первая → последняя)")
    
    # Общая статистика
    if all_totals:
        print("\n" + "="*90)
        print("ОБЩАЯ СТАТИСТИКА (СРЕДНЕЕ ПО ВСЕМ РЕШЕНИЯМ)")
        print("="*90)
        
        avg_total_all = statistics.mean(all_totals)
        
        for stage_key, stage_name in stage_names.items():
            times = all_stages.get(stage_key, [])
            if times:
                avg_time = statistics.mean(times)
                percentage = (avg_time / avg_total_all) * 100
                
                print(f"\n  {stage_name}:")
                print(f"    Время:     {format_time(avg_time):>12}")
                print(f"    Процент:   {percentage:>11.1f}%")
        
        print(f"\n  Общее среднее время решения:")
        print(f"    {format_time(avg_total_all)}")
        
        print(f"\n  Статистика по решениям:")
        print(f"    Всего решений: {len(all_totals)}")
        print(f"    Уникальных переменных: {len(var_stats)}")

def analyze_convergence(filename):
    """Анализирует сходимость из лога"""
    
    # Поиск информации о сходимости
    patterns = {
        'iterations': r'Iterations\s+=\s+(\d+)',
        'residual': r'Final residual\s+=\s+([\d.e+-]+)',
        'norm': r'norm\s+=\s+([\d.e+-]+)'
    }
    
    with open(filename, 'r') as f:
        content = f.read()
    
    for name, pattern in patterns.items():
        matches = re.findall(pattern, content)
        if matches:
            print(f"\n  {name}: {matches[-5:]}")  # Последние 5 значений

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_petsc_timings.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    
    try:
        solutions = parse_log(log_file)
        print(f"Найдено решений: {len(solutions)}")
        
        if solutions:
            # Показываем первые несколько решений
            print("\nПервые 5 решений:")
            for i, sol in enumerate(solutions[:5]):
                print(f"  {i+1}: {sol['variable']} (итер. {sol['iteration']})")
        
        var_stats = calculate_durations(solutions)
        print_statistics(var_stats)
        
        # Дополнительный анализ сходимости (опционально)
        analyze_convergence(log_file)
        
    except FileNotFoundError:
        print(f"Файл {log_file} не найден!")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()