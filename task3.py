import timeit
from collections import defaultdict

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

text1 = "article_1.txt"
text2 = "article_2.txt"

existing_substring = "алгоритми"
nonexistent_substring = "qwertyxyz"

def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j  # Знайдено
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1  # Не знайдено

def boyer_moore_search(text, pattern):
    bad_char = defaultdict(lambda: -1)
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i

    shift = 0
    while shift <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        if j < 0:
            return shift  # Знайдено
        else:
            shift += max(1, j - bad_char[text[shift + j]])
    return -1  # Не знайдено

def rabin_karp_search(text, pattern, prime=101):
    d = 256  # Розмір алфавіту
    m, n = len(pattern), len(text)
    h, t, p = 1, 0, 0
    for i in range(m - 1):
        h = (h * d) % prime
    for i in range(m):
        p = (d * p + ord(pattern[i])) % prime
        t = (d * t + ord(text[i])) % prime
    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                return i  # Знайдено
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t < 0:
                t += prime
    return -1  # Не знайдено

def measure_time(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=10)

results = {}
for text_name, text in [("Стаття 1", text1), ("Стаття 2", text2)]:
    for substring_type, substring in [("існуючий", existing_substring), ("вигаданий", nonexistent_substring)]:
        results[(text_name, substring_type)] = {
            "КМП": measure_time(kmp_search, text, substring),
            "Боєр-Мур": measure_time(boyer_moore_search, text, substring),
            "Рабін-Карп": measure_time(rabin_karp_search, text, substring)
        }

for key, times in results.items():
    print(f"Текст: {key[0]}, Підрядок: {key[1]}")
    for algo, time in times.items():
        print(f"  {algo}: {time:.6f} сек")
    print()
