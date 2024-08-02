import time
from tabulate import tabulate

class CoinChangeError(Exception):
    """Користувацький виняток для помилок у процесі видачі решти."""
    pass

def find_coins_greedy(amount):
    """
    Знаходить кількість монет кожного номіналу для формування заданої суми за допомогою жадібного алгоритму.

    :param amount: Сума для видачі решти.
    :return: Словник з кількістю монет кожного номіналу.
    :raises CoinChangeError: Якщо вхідні дані некоректні.
    """
    if not isinstance(amount, int) or amount < 0:
        raise CoinChangeError("Сума має бути додатнім цілим числом.")

    coins = [50, 25, 10, 5, 2, 1]
    result = {}
    
    for coin in coins:
        if amount >= coin:
            num_coins = amount // coin
            amount -= num_coins * coin
            result[coin] = num_coins
    
    return result

def find_min_coins(amount):
    """
    Знаходить мінімальну кількість монет для формування заданої суми за допомогою алгоритму динамічного програмування.

    :param amount: Сума для видачі решти.
    :return: Словник з кількістю монет кожного номіналу.
    :raises CoinChangeError: Якщо вхідні дані некоректні.
    """
    if not isinstance(amount, int) or amount < 0:
        raise CoinChangeError("Сума має бути додатнім цілим числом.")

    coins = [1, 2, 5, 10, 25, 50]
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    used_coins = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    used_coins[i] = coin

    if dp[amount] == float('inf'):
        raise CoinChangeError("Неможливо сформувати задану суму з доступних монет.")

    result = {}
    while amount > 0:
        coin = used_coins[amount]
        if coin in result:
            result[coin] += 1
        else:
            result[coin] = 1
        amount -= coin

    return result

def format_result_table(results):
    """
    Форматує результати у вигляді таблиці.

    :param results: Словник з кількістю монет кожного номіналу.
    :return: Таблиця у вигляді рядка.
    """
    table_data = []
    for coin, count in sorted(results.items(), reverse=True):
        table_data.append([coin, count])
    
    return tabulate(table_data, headers=["Номінал", "Кількість"], tablefmt="grid")

def compare_algorithms(amount):
    results = []

    # Жадібний алгоритм
    try:
        start_time = time.time()
        greedy_result = find_coins_greedy(amount)
        greedy_time = time.time() - start_time
        greedy_table = format_result_table(greedy_result)
        results.append(["Жадібний алгоритм", greedy_table, greedy_time])
    except CoinChangeError as e:
        results.append(["Жадібний алгоритм", str(e), "N/A"])

    # Алгоритм динамічного програмування
    try:
        start_time = time.time()
        dp_result = find_min_coins(amount)
        dp_time = time.time() - start_time
        dp_table = format_result_table(dp_result)
        results.append(["Динамічне програмування", dp_table, dp_time])
    except CoinChangeError as e:
        results.append(["Динамічне програмування", str(e), "N/A"])

    return results

def main():
    amounts = [113, 289, 523, 999]  # Різні суми для тестування
    for amount in amounts:
        print(f"\nСума: {amount}")
        comparison_results = compare_algorithms(amount)
        print(tabulate(comparison_results, headers=["Алгоритм", "Результат", "Час виконання (секунди)"], tablefmt="grid"))

if __name__ == "__main__":
    main()
