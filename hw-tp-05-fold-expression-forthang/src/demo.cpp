#include "base_interface.hpp"
#include <iostream>
#include <string>
#include <vector>
#include <typeinfo>

// Вспомогательная функция для получения имени типа
template<typename T>
std::string type_name() {
    return typeid(T).name();
}

int main() {
    std::cout << "=== Fold Expressions Demo: for_each_in_tuple & tuple_transform ===\n\n";
    
    // Создаем кортеж с разными типами
    auto mixed_tuple = std::make_tuple(42, 3.14, std::string("Hello"), 'A', true);
    
    std::cout << "Original tuple: (42, 3.14, \"Hello\", 'A', true)\n\n";
    
    // 1. Демонстрация for_each_in_tuple
    std::cout << "1. for_each_in_tuple demonstration:\n";
    std::cout << "   Printing each element with its index:\n";
    
    int index = 0;
    auto printer = [&index](const auto& value) {
        std::cout << "   [" << index++ << "] = " << value 
                  << " (type: " << type_name<std::decay_t<decltype(value)>>() << ")\n";
    };
    
    for_each_in_tuple(mixed_tuple, printer);
    
    // 2. Подсчет элементов
    std::cout << "\n2. Counting elements:\n";
    int count = 0;
    auto counter = [&count](const auto&) { count++; };
    
    for_each_in_tuple(mixed_tuple, counter);
    std::cout << "   Total elements: " << count << "\n";
    
    // 3. Условная обработка
    std::cout << "\n3. Conditional processing (sum numeric values):\n";
    double sum = 0.0;
    auto numeric_summer = [&sum](const auto& value) {
        using T = std::decay_t<decltype(value)>;
        if constexpr (std::is_arithmetic_v<T> && !std::is_same_v<T, bool> && !std::is_same_v<T, char>) {
            sum += static_cast<double>(value);
            std::cout << "   Added " << value << " to sum\n";
        }
    };
    
    for_each_in_tuple(mixed_tuple, numeric_summer);
    std::cout << "   Total sum: " << sum << "\n";
    
    // 4. Демонстрация tuple_transform
    std::cout << "\n4. tuple_transform demonstration:\n";
    
    // Преобразование в строки
    std::cout << "   Converting all elements to strings:\n";
    auto to_string_func = [](const auto& value) {
        if constexpr (std::is_same_v<std::decay_t<decltype(value)>, std::string>) {
            return value;
        } else if constexpr (std::is_same_v<std::decay_t<decltype(value)>, char>) {
            return std::string(1, value);
        } else if constexpr (std::is_same_v<std::decay_t<decltype(value)>, bool>) {
            return value ? std::string("true") : std::string("false");
        } else {
            return std::to_string(value);
        }
    };
    
    auto string_tuple = tuple_transform(mixed_tuple, to_string_func);
    
    std::cout << "   String tuple: ";
    for_each_in_tuple(string_tuple, [](const auto& str) {
        std::cout << "\"" << str << "\" ";
    });
    std::cout << "\n";
    
    // 5. Математические преобразования
    std::cout << "\n5. Mathematical transformations:\n";
    auto numbers = std::make_tuple(1, 2, 3, 4, 5);
    
    auto squarer = [](const auto& value) {
        return value * value;
    };
    
    auto squared = tuple_transform(numbers, squarer);
    
    std::cout << "   Original: ";
    for_each_in_tuple(numbers, [](const auto& n) {
        std::cout << n << " ";
    });
    std::cout << "\n   Squared:  ";
    for_each_in_tuple(squared, [](const auto& n) {
        std::cout << n << " ";
    });
    std::cout << "\n";
    
    // 6. Работа с пустым кортежем
    std::cout << "\n6. Empty tuple handling:\n";
    auto empty = std::make_tuple();
    int empty_count = 0;
    
    for_each_in_tuple(empty, [&empty_count](const auto&) { empty_count++; });
    std::cout << "   Empty tuple element count: " << empty_count << "\n";
    
    auto empty_transformed = tuple_transform(empty, [](const auto& x) { return x; });
    std::cout << "   Empty tuple transformation: success\n";
    
    // 7. Compile-time проверки
    std::cout << "\n7. Compile-time checks:\n";
    static_assert(std::tuple_size_v<decltype(mixed_tuple)> == 5);
    static_assert(std::tuple_size_v<decltype(empty)> == 0);
    static_assert(std::tuple_size_v<decltype(squared)> == 5);
    
    std::cout << "   ✓ All static_assert checks passed!\n";
    
    std::cout << "\n=== Demo completed ===\n";
    return 0;
}
