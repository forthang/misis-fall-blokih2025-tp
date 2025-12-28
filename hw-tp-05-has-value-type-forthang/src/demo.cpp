#include "base_interface.hpp"
#include <iostream>
#include <vector>
#include <list>
#include <string>
#include <array>

// Пользовательские типы для демонстрации
struct ContainerLike {
    using value_type = int;
    int* begin() { return nullptr; }
    int* end() { return nullptr; }
};

struct IterableLike {
    int* begin() { return nullptr; }
    int* end() { return nullptr; }
    // Нет value_type
};

struct ValueTypeLike {
    using value_type = double;
    // Нет begin()
};

struct PlainType {
    int data;
    // Ни value_type, ни begin()
};

template<typename T>
void check_type(const std::string& type_name) {
    std::cout << type_name << ":\n";
    std::cout << "  HasValueType: " << (HasValueType_v<T> ? "✓" : "✗") << "\n";
    std::cout << "  HasBegin:     " << (HasBegin_v<T> ? "✓" : "✗") << "\n\n";
}

int main() {
    std::cout << "=== Type Traits Demo: HasValueType & HasBegin ===\n\n";
    
    std::cout << "Standard Library Containers:\n";
    std::cout << "-----------------------------\n";
    check_type<std::vector<int>>("std::vector<int>");
    check_type<std::list<double>>("std::list<double>");
    check_type<std::string>("std::string");
    check_type<std::array<int, 5>>("std::array<int, 5>");
    
    std::cout << "Built-in Types:\n";
    std::cout << "---------------\n";
    check_type<int>("int");
    check_type<double>("double");
    check_type<int*>("int*");
    check_type<char[]>("char[]");
    
    std::cout << "Custom Types:\n";
    std::cout << "-------------\n";
    check_type<ContainerLike>("ContainerLike (has both)");
    check_type<IterableLike>("IterableLike (has begin only)");
    check_type<ValueTypeLike>("ValueTypeLike (has value_type only)");
    check_type<PlainType>("PlainType (has neither)");
    
    // Compile-time проверки
    std::cout << "Compile-time Assertions:\n";
    std::cout << "------------------------\n";
    
    // Проверки HasValueType
    static_assert(HasValueType_v<std::vector<int>>);
    static_assert(!HasValueType_v<int>);
    static_assert(HasValueType_v<ContainerLike>);
    static_assert(!HasValueType_v<PlainType>);
    
    // Проверки HasBegin
    static_assert(HasBegin_v<std::vector<int>>);
    static_assert(!HasBegin_v<int>);
    static_assert(HasBegin_v<ContainerLike>);
    static_assert(!HasBegin_v<PlainType>);
    
    std::cout << "✓ All static_assert checks passed!\n\n";
    
    // Практическое применение
    std::cout << "Practical Usage Example:\n";
    std::cout << "------------------------\n";
    
    auto process_container = [](auto&& container) {
        using T = std::decay_t<decltype(container)>;
        
        if constexpr (HasValueType_v<T> && HasBegin_v<T>) {
            std::cout << "Processing as full container (has value_type and begin)\n";
        } else if constexpr (HasBegin_v<T>) {
            std::cout << "Processing as iterable (has begin only)\n";
        } else if constexpr (HasValueType_v<T>) {
            std::cout << "Processing as value holder (has value_type only)\n";
        } else {
            std::cout << "Processing as plain type\n";
        }
    };
    
    std::vector<int> vec;
    IterableLike iterable;
    ValueTypeLike value_holder;
    PlainType plain;
    
    process_container(vec);
    process_container(iterable);
    process_container(value_holder);
    process_container(plain);
    
    std::cout << "\n=== Demo completed ===\n";
    return 0;
}
