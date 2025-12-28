#include "gtest/gtest.h"
#include "base_interface.hpp"
#include <list>
#include <string>
#include <array>

// Тесты для HasValueType
TEST(HasValueTypeTest, VectorHasValueType) {
    EXPECT_TRUE(HasValueType<std::vector<int>>::value);
    EXPECT_TRUE(HasValueType_v<std::vector<int>>);
}

TEST(HasValueTypeTest, IntDoesNotHaveValueType) {
    EXPECT_FALSE(HasValueType<int>::value);
    EXPECT_FALSE(HasValueType_v<int>);
}

TEST(HasValueTypeTest, ListHasValueType) {
    EXPECT_TRUE(HasValueType<std::list<double>>::value);
    EXPECT_TRUE(HasValueType_v<std::list<double>>);
}

TEST(HasValueTypeTest, StringHasValueType) {
    EXPECT_TRUE(HasValueType<std::string>::value);
    EXPECT_TRUE(HasValueType_v<std::string>);
}

TEST(HasValueTypeTest, ArrayHasValueType) {
    using ArrayType = std::array<int, 5>;
    EXPECT_TRUE(HasValueType<ArrayType>::value);
    EXPECT_TRUE(HasValueType_v<ArrayType>);
}

TEST(HasValueTypeTest, PointerDoesNotHaveValueType) {
    EXPECT_FALSE(HasValueType<int*>::value);
    EXPECT_FALSE(HasValueType_v<int*>);
}

// Тесты для HasBegin (дополнительное задание)
TEST(HasBeginTest, VectorHasBegin) {
    EXPECT_TRUE(HasBegin<std::vector<int>>::value);
    EXPECT_TRUE(HasBegin_v<std::vector<int>>);
}

TEST(HasBeginTest, IntDoesNotHaveBegin) {
    EXPECT_FALSE(HasBegin<int>::value);
    EXPECT_FALSE(HasBegin_v<int>);
}

TEST(HasBeginTest, ListHasBegin) {
    EXPECT_TRUE(HasBegin<std::list<double>>::value);
    EXPECT_TRUE(HasBegin_v<std::list<double>>);
}

TEST(HasBeginTest, StringHasBegin) {
    EXPECT_TRUE(HasBegin<std::string>::value);
    EXPECT_TRUE(HasBegin_v<std::string>);
}

TEST(HasBeginTest, ArrayHasBegin) {
    using ArrayType = std::array<int, 5>;
    EXPECT_TRUE(HasBegin<ArrayType>::value);
    EXPECT_TRUE(HasBegin_v<ArrayType>);
}

// Тест с пользовательским типом
struct CustomContainer {
    using value_type = int;
    int* begin() { return nullptr; }
    int* end() { return nullptr; }
};

struct CustomTypeWithoutValueType {
    int* begin() { return nullptr; }
    int* end() { return nullptr; }
};

struct CustomTypeWithoutBegin {
    using value_type = int;
};

TEST(HasValueTypeTest, CustomContainerHasValueType) {
    EXPECT_TRUE(HasValueType_v<CustomContainer>);
}

TEST(HasValueTypeTest, CustomTypeWithoutValueTypeDoesNotHaveValueType) {
    EXPECT_FALSE(HasValueType_v<CustomTypeWithoutValueType>);
}

TEST(HasBeginTest, CustomContainerHasBegin) {
    EXPECT_TRUE(HasBegin_v<CustomContainer>);
}

TEST(HasBeginTest, CustomTypeWithoutValueTypeHasBegin) {
    EXPECT_TRUE(HasBegin_v<CustomTypeWithoutValueType>);
}

TEST(HasBeginTest, CustomTypeWithoutBeginDoesNotHaveBegin) {
    EXPECT_FALSE(HasBegin_v<CustomTypeWithoutBegin>);
}
