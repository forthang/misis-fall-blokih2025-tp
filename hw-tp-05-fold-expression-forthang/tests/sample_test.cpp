#include "gtest/gtest.h"
#include "base_interface.hpp"
#include <vector>

TEST(ForEachInTupleTest, AppliesFunctionToAllElements) {
    auto my_tuple = std::make_tuple(1, 2.5, std::string("Test"));
    int call_count = 0;
    int sum = 0;

    auto counter_and_summer = [&](const auto& value) {
        call_count++;
        // Используем constexpr if для условного суммирования только числовых типов
        if constexpr (std::is_integral_v<std::decay_t<decltype(value)>>) {
            sum += value;
        }
    };

    for_each_in_tuple(my_tuple, counter_and_summer);

    // Проверяем, что функция была вызвана 3 раза (по количеству элементов)
    EXPECT_EQ(call_count, 3);

    // Проверяем, что целочисленный элемент был просуммирован
    EXPECT_EQ(sum, 1);
}

TEST(ForEachInTupleTest, WorksWithEmptyTuple) {
    auto empty_tuple = std::make_tuple();
    int call_count = 0;

    auto counter = [&](const auto&) {
        call_count++;
    };

    for_each_in_tuple(empty_tuple, counter);
    EXPECT_EQ(call_count, 0);
}

TEST(ForEachInTupleTest, WorksWithSingleElement) {
    auto single_tuple = std::make_tuple(42);
    int result = 0;

    auto extractor = [&](const auto& value) {
        result = value;
    };

    for_each_in_tuple(single_tuple, extractor);
    EXPECT_EQ(result, 42);
}

TEST(ForEachInTupleTest, PreservesOrder) {
    auto tuple = std::make_tuple(1, 2, 3, 4, 5);
    std::vector<int> results;

    auto collector = [&](const auto& value) {
        results.push_back(value);
    };

    for_each_in_tuple(tuple, collector);
    
    std::vector<int> expected = {1, 2, 3, 4, 5};
    EXPECT_EQ(results, expected);
}

TEST(ForEachInTupleTest, WorksWithConstTuple) {
    const auto const_tuple = std::make_tuple(10, 20.5, std::string("const"));
    int call_count = 0;

    auto counter = [&](const auto&) {
        call_count++;
    };

    for_each_in_tuple(const_tuple, counter);
    EXPECT_EQ(call_count, 3);
}

TEST(ForEachInTupleTest, WorksWithRValueTuple) {
    int call_count = 0;

    auto counter = [&](const auto&) {
        call_count++;
    };

    for_each_in_tuple(std::make_tuple(1, 2.0, "rvalue"), counter);
    EXPECT_EQ(call_count, 3);
}

// Тесты для дополнительного задания - tuple_transform
TEST(TupleTransformTest, TransformsAllElements) {
    auto original = std::make_tuple(1, 2, 3);
    
    auto doubler = [](const auto& value) {
        return value * 2;
    };

    auto transformed = tuple_transform(original, doubler);
    auto expected = std::make_tuple(2, 4, 6);
    
    EXPECT_EQ(transformed, expected);
}

TEST(TupleTransformTest, ChangesTypes) {
    auto original = std::make_tuple(1, 2, 3);
    
    auto to_string = [](const auto& value) {
        return std::to_string(value);
    };

    auto transformed = tuple_transform(original, to_string);
    auto expected = std::make_tuple(std::string("1"), std::string("2"), std::string("3"));
    
    EXPECT_EQ(transformed, expected);
}

TEST(TupleTransformTest, WorksWithEmptyTuple) {
    auto empty = std::make_tuple();
    
    auto identity = [](const auto& value) {
        return value;
    };

    auto transformed = tuple_transform(empty, identity);
    auto expected = std::make_tuple();
    
    EXPECT_EQ(transformed, expected);
}

TEST(TupleTransformTest, WorksWithMixedTypes) {
    auto mixed = std::make_tuple(42, 3.14, std::string("hello"));
    
    auto type_info = [](const auto& value) {
        using T = std::decay_t<decltype(value)>;
        if constexpr (std::is_integral_v<T>) {
            return std::string("int");
        } else if constexpr (std::is_floating_point_v<T>) {
            return std::string("float");
        } else {
            return std::string("other");
        }
    };

    auto transformed = tuple_transform(mixed, type_info);
    auto expected = std::make_tuple(std::string("int"), std::string("float"), std::string("other"));
    
    EXPECT_EQ(transformed, expected);
}
