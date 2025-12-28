#include "base_interface.hpp"
#include <iostream>
#include <typeinfo>
#include <string>

// Вспомогательная функция для получения имени типа
template<typename T>
std::string type_name() {
    return typeid(T).name();
}

int main() {
    std::cout << "=== TypeList Metafunctions Demo ===\n\n";
    
    // Определяем список типов
    using MyList = TypeList<int, double, std::string, char, bool>;
    
    std::cout << "Original TypeList: TypeList<int, double, std::string, char, bool>\n\n";
    
    // Демонстрация GetTypeAtIndex
    std::cout << "1. GetTypeAtIndex demonstration:\n";
    std::cout << "   Index 0: " << type_name<typename GetTypeAtIndex<0, MyList>::type>() << " (int)\n";
    std::cout << "   Index 1: " << type_name<typename GetTypeAtIndex<1, MyList>::type>() << " (double)\n";
    std::cout << "   Index 2: " << type_name<typename GetTypeAtIndex<2, MyList>::type>() << " (std::string)\n";
    std::cout << "   Index 3: " << type_name<typename GetTypeAtIndex<3, MyList>::type>() << " (char)\n";
    std::cout << "   Index 4: " << type_name<typename GetTypeAtIndex<4, MyList>::type>() << " (bool)\n\n";
    
    // Демонстрация Concat
    std::cout << "2. Concat demonstration:\n";
    using List1 = TypeList<int, double>;
    using List2 = TypeList<float, char>;
    using ConcatResult = typename Concat<List1, List2>::type;
    
    std::cout << "   List1: TypeList<int, double>\n";
    std::cout << "   List2: TypeList<float, char>\n";
    std::cout << "   Concat result: TypeList<int, double, float, char>\n";
    std::cout << "   Verification - Index 2 of result: " 
              << type_name<typename GetTypeAtIndex<2, ConcatResult>::type>() << " (float)\n\n";
    
    // Демонстрация RemoveAt
    std::cout << "3. RemoveAt demonstration:\n";
    using RemoveResult0 = typename RemoveAt<0, MyList>::type;  // Удаляем int
    using RemoveResult2 = typename RemoveAt<2, MyList>::type;  // Удаляем std::string
    
    std::cout << "   Original: TypeList<int, double, std::string, char, bool>\n";
    std::cout << "   RemoveAt<0>: TypeList<double, std::string, char, bool>\n";
    std::cout << "   Verification - Index 0 after removal: " 
              << type_name<typename GetTypeAtIndex<0, RemoveResult0>::type>() << " (double)\n";
    
    std::cout << "   RemoveAt<2>: TypeList<int, double, char, bool>\n";
    std::cout << "   Verification - Index 2 after removal: " 
              << type_name<typename GetTypeAtIndex<2, RemoveResult2>::type>() << " (char)\n\n";
    
    // Compile-time проверки
    std::cout << "4. Compile-time type checking:\n";
    static_assert(std::is_same_v<typename GetTypeAtIndex<0, MyList>::type, int>);
    static_assert(std::is_same_v<typename GetTypeAtIndex<2, MyList>::type, std::string>);
    static_assert(std::is_same_v<typename RemoveAt<0, MyList>::type, TypeList<double, std::string, char, bool>>);
    
    std::cout << "   ✓ All static_assert checks passed at compile time!\n";
    
    std::cout << "\n=== Demo completed successfully ===\n";
    return 0;
}
