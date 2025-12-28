#include "base_interface.hpp"
#include "gtest/gtest.h"

// Тест на извлечение типа по индексу
TEST(GetTypeAtIndexTest, ExtractsCorrectType) {
    using MyList = TypeList<int, double, float, char>;

    // Проверяем, что тип на позиции 0 - int
    using Type0 = typename GetTypeAtIndex<0, MyList>::type;
    EXPECT_TRUE((std::is_same_v<Type0, int>));

    // Проверяем, что тип на позиции 1 - double
    using Type1 = typename GetTypeAtIndex<1, MyList>::type;
    EXPECT_TRUE((std::is_same_v<Type1, double>));

    // Проверяем, что тип на позиции 2 - float
    using Type2 = typename GetTypeAtIndex<2, MyList>::type;
    EXPECT_TRUE((std::is_same_v<Type2, float>));

    // Проверяем, что тип на позиции 3 - char
    using Type3 = typename GetTypeAtIndex<3, MyList>::type;
    EXPECT_TRUE((std::is_same_v<Type3, char>));
}

// Тест с одним элементом
TEST(GetTypeAtIndexTest, SingleElement) {
    using SingleList = TypeList<bool>;
    
    using Type0 = typename GetTypeAtIndex<0, SingleList>::type;
    EXPECT_TRUE((std::is_same_v<Type0, bool>));
}

// Тест с различными типами
TEST(GetTypeAtIndexTest, DifferentTypes) {
    using ComplexList = TypeList<std::vector<int>, const char*, std::string>;
    
    using Type0 = typename GetTypeAtIndex<0, ComplexList>::type;
    EXPECT_TRUE((std::is_same_v<Type0, std::vector<int>>));
    
    using Type1 = typename GetTypeAtIndex<1, ComplexList>::type;
    EXPECT_TRUE((std::is_same_v<Type1, const char*>));
    
    using Type2 = typename GetTypeAtIndex<2, ComplexList>::type;
    EXPECT_TRUE((std::is_same_v<Type2, std::string>));
}

// Тесты для Concat
TEST(ConcatTest, ConcatenatesTwoLists) {
    using List1 = TypeList<int, double>;
    using List2 = TypeList<float, char>;
    using Expected = TypeList<int, double, float, char>;
    
    using Result = typename Concat<List1, List2>::type;
    EXPECT_TRUE((std::is_same_v<Result, Expected>));
}

TEST(ConcatTest, ConcatenateWithEmptyList) {
    using List1 = TypeList<int, double>;
    using List2 = TypeList<>;
    
    using Result = typename Concat<List1, List2>::type;
    EXPECT_TRUE((std::is_same_v<Result, List1>));
}

// Тесты для RemoveAt
TEST(RemoveAtTest, RemoveFirstElement) {
    using Original = TypeList<int, double, float, char>;
    using Expected = TypeList<double, float, char>;
    
    using Result = typename RemoveAt<0, Original>::type;
    EXPECT_TRUE((std::is_same_v<Result, Expected>));
}

TEST(RemoveAtTest, RemoveMiddleElement) {
    using Original = TypeList<int, double, float, char>;
    using Expected = TypeList<int, float, char>;
    
    using Result = typename RemoveAt<1, Original>::type;
    EXPECT_TRUE((std::is_same_v<Result, Expected>));
}

TEST(RemoveAtTest, RemoveLastElement) {
    using Original = TypeList<int, double, float, char>;
    using Expected = TypeList<int, double, float>;
    
    using Result = typename RemoveAt<3, Original>::type;
    EXPECT_TRUE((std::is_same_v<Result, Expected>));
}

TEST(RemoveAtTest, RemoveFromSingleElement) {
    using Original = TypeList<int>;
    using Expected = TypeList<>;
    
    using Result = typename RemoveAt<0, Original>::type;
    EXPECT_TRUE((std::is_same_v<Result, Expected>));
}
