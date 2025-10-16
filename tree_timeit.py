"""
сравнение производительности рекурсивного и итеративного построения бинарных деревьев

этот модуль сравнивает время выполнения двух подходов к построению бинарных деревьев:
- рекурсивный подход: использует рекурсивные вызовы для построения поддеревьев
- итеративный подход: использует очередь для обхода уровней дерева
"""

import timeit
import matplotlib.pyplot as plt
from collections import deque
import random


def left_branch(root):
    return root * 3 + 1


def right_branch(root):
    return 3 * root - 1


# рекурсивная функция
def build_tree_recursive(height, root=10, l_b=left_branch, r_b=right_branch):
    if height <= 0:
        return {f'{root}': []}
    else:
        left_val, right_val = l_b(root), r_b(root)
        return {
            f'{root}': [
                build_tree_recursive(height - 1, left_val, l_b=l_b, r_b=r_b),
                build_tree_recursive(height - 1, right_val, l_b=l_b, r_b=r_b)
            ]
        }


# нерекурсивная функция
def build_tree_iterative(height=5, root=10, lt_branch=left_branch, rt_branch=right_branch):
    if height <= 0:
        return {str(root): []}
    tree = {}
    queue = deque([(root, 1)])

    while queue:
        current_root, current_height = queue.popleft()
        root_key = str(current_root)

        if current_height < height:
            left_val = lt_branch(current_root)
            right_val = rt_branch(current_root)

            tree[root_key] = [str(left_val), str(right_val)]

            queue.append((left_val, current_height + 1))
            queue.append((right_val, current_height + 1))
        else:
            pass
    return tree


# функция для сравнения производительности
def benchmark(func, data, repeat=5):
    """
    Измеряет среднее время выполнения функции на наборе данных,
    для каждого элемента данных функция запускается несколько раз,
    берется минимальное время (чтобы исключить влияние фоновых процессов),
    затем результаты усредняются

    args:
        func (callable): функция для тестирования
        data (list): набор входных данных
        repeat (int): количество повторений для каждого элемента данных

    returns:
        float: среднее время выполнения в секундах
    """
    total = 0
    for n in data:
        # запускаем функцию repeat раз и берем лучшее время
        times = timeit.repeat(lambda: func(n), number=1, repeat=repeat)
        total += min(times)
    return total / len(data)


def main():
    test_heights = list(range(1, 11))
    res_recursive = []
    res_iterative = []

    for height in test_heights:
        res_recursive.append(benchmark(build_tree_recursive, [height]))
        res_iterative.append(benchmark(build_tree_iterative, [height]))

    # простой вывод
    print("\nРекурсивная реализация:")
    for i, height in enumerate(test_heights):
        print(f"Высота {height}: {res_recursive[i]:.6f} сек")

    print("\nИтеративная реализация:")
    for i, height in enumerate(test_heights):
        print(f"Высота {height}: {res_iterative[i]:.6f} сек")

    # визуализация
    plt.plot(test_heights, res_recursive, label="Рекурсивная")
    plt.plot(test_heights, res_iterative, label="Итеративная")
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение производительности")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
