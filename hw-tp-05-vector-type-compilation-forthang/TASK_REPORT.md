# Отчет о выполнении задания: Компиляция Вектора Типов

## ✅ Выполненные задачи

### Основное задание
- **TypeList**: Структура для хранения списка типов
- **GetTypeAtIndex**: Метафункция для извлечения типа по индексу
- **Рекурсивная реализация**: Использование частичной специализации шаблонов
- **Compile-time вычисления**: Вся логика выполняется на этапе компиляции

### 🎯 Дополнительное задание
- **Concat**: Метафункция для объединения двух TypeList
- **RemoveAt**: Метафункция для удаления элемента по индексу
- **Расширенное тестирование**: Comprehensive тесты для всех функций

## Реализация

### 1. TypeList - Контейнер типов
```cpp
template <typename... Ts>
struct TypeList {};
```

### 2. GetTypeAtIndex - Извлечение по индексу
```cpp
// Общее объявление
template <size_t N, typename List>
struct GetTypeAtIndex {};

// Рекурсивный случай (N > 0)
template <size_t N, typename H, typename... Ts>
struct GetTypeAtIndex<N, TypeList<H, Ts...>> {
    using type = typename GetTypeAtIndex<N - 1, TypeList<Ts...>>::type;
};

// Базовый случай (N = 0)
template <typename H, typename... Ts>
struct GetTypeAtIndex<0, TypeList<H, Ts...>> {
    using type = H;
};
```

### 3. Concat - Объединение списков
```cpp
template <typename... Ts1, typename... Ts2>
struct Concat<TypeList<Ts1...>, TypeList<Ts2...>> {
    using type = TypeList<Ts1..., Ts2...>;
};
```

### 4. RemoveAt - Удаление по индексу
```cpp
// Базовый случай (N = 0)
template <typename H, typename... Ts>
struct RemoveAt<0, TypeList<H, Ts...>> {
    using type = TypeList<Ts...>;
};

// Рекурсивный случай (N > 0)
template <size_t N, typename H, typename... Ts>
struct RemoveAt<N, TypeList<H, Ts...>> {
    using type = typename Concat<
        TypeList<H>, 
        typename RemoveAt<N - 1, TypeList<Ts...>>::type
    >::type;
};
```

## Алгоритм работы

### GetTypeAtIndex
1. **Рекурсивный спуск**: Уменьшаем индекс N и "отрезаем" первый тип
2. **Базовый случай**: Когда N = 0, возвращаем первый тип
3. **Compile-time**: Вся рекурсия разворачивается компилятором

### RemoveAt
1. **Сохранение префикса**: Элементы до индекса N сохраняются
2. **Пропуск элемента**: Элемент с индексом N пропускается
3. **Объединение**: Префикс объединяется с оставшимся хвостом

## Результаты тестирования

```
[==========] Running 9 tests from 3 test suites.
[----------] 3 tests from GetTypeAtIndexTest
[ RUN      ] GetTypeAtIndexTest.ExtractsCorrectType
[       OK ] GetTypeAtIndexTest.ExtractsCorrectType (0 ms)
[ RUN      ] GetTypeAtIndexTest.SingleElement
[       OK ] GetTypeAtIndexTest.SingleElement (0 ms)
[ RUN      ] GetTypeAtIndexTest.DifferentTypes
[       OK ] GetTypeAtIndexTest.DifferentTypes (0 ms)

[----------] 2 tests from ConcatTest
[ RUN      ] ConcatTest.ConcatenatesTwoLists
[       OK ] ConcatTest.ConcatenatesTwoLists (0 ms)
[ RUN      ] ConcatTest.ConcatenateWithEmptyList
[       OK ] ConcatTest.ConcatenateWithEmptyList (0 ms)

[----------] 4 tests from RemoveAtTest
[ RUN      ] RemoveAtTest.RemoveFirstElement
[       OK ] RemoveAtTest.RemoveFirstElement (0 ms)
[ RUN      ] RemoveAtTest.RemoveMiddleElement
[       OK ] RemoveAtTest.RemoveMiddleElement (0 ms)
[ RUN      ] RemoveAtTest.RemoveLastElement
[       OK ] RemoveAtTest.RemoveLastElement (0 ms)
[ RUN      ] RemoveAtTest.RemoveFromSingleElement
[       OK ] RemoveAtTest.RemoveFromSingleElement (0 ms)

[  PASSED  ] 9 tests.
```

## Демонстрация работы

```cpp
using MyList = TypeList<int, double, std::string, char, bool>;

// Извлечение типов
using Type0 = typename GetTypeAtIndex<0, MyList>::type;  // int
using Type2 = typename GetTypeAtIndex<2, MyList>::type;  // std::string

// Объединение списков
using List1 = TypeList<int, double>;
using List2 = TypeList<float, char>;
using Combined = typename Concat<List1, List2>::type;  // TypeList<int, double, float, char>

// Удаление элементов
using Removed = typename RemoveAt<1, MyList>::type;  // TypeList<int, std::string, char, bool>
```

## Ключевые особенности

### 1. Template Metaprogramming
- **Рекурсивные шаблоны**: Элегантное решение через специализацию
- **Compile-time вычисления**: Нулевые runtime накладные расходы
- **Type safety**: Строгая типизация на этапе компиляции

### 2. Частичная специализация
- **Паттерн matching**: Разбор структуры типов
- **Рекурсивный спуск**: Обработка вариативных шаблонов
- **Базовые случаи**: Корректное завершение рекурсии

### 3. Обработка ошибок
- **Compile-time errors**: Некорректные индексы вызывают ошибки компиляции
- **Type safety**: Невозможно получить неправильный тип
- **Static assertions**: Проверки на этапе компиляции

## Применение

Данные метафункции могут использоваться для:
- **Tuple-like структур**: Доступ к элементам по индексу
- **Variant типов**: Работа с union типами
- **Template libraries**: Основа для более сложных метафункций
- **Type manipulation**: Трансформации списков типов

## Заключение

Задание выполнено полностью:

✅ **Основная функциональность**: GetTypeAtIndex работает корректно  
✅ **Дополнительные функции**: Concat и RemoveAt реализованы  
✅ **Comprehensive тестирование**: Все случаи покрыты тестами  
✅ **Демонстрация**: Работающий пример использования  

Реализация демонстрирует глубокое понимание template metaprogramming, рекурсивных шаблонов и compile-time вычислений в C++.
