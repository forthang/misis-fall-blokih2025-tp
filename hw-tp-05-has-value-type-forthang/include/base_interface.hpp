#include <vector>
#include <type_traits>

// --- РЕАЛИЗАЦИЯ ЗАДАЧИ ---

// 1. Объявляем общий шаблон.
template <typename T, typename = std::void_t<>>
struct HasValueType_Impl : std::false_type {};

// 2. Частичная специализация, которая выбирается, если подстановка T::value_type успешна.
template <typename T>
struct HasValueType_Impl<T, std::void_t<typename T::value_type>> : std::true_type {};

// Основной публичный trait
template <typename T>
using HasValueType = HasValueType_Impl<T>;

// Вспомогательная переменная (C++17)
template<typename T>
inline constexpr bool HasValueType_v = HasValueType<T>::value;

// --- ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ ---

// Проверка наличия функции-члена begin()
template <typename T, typename = std::void_t<>>
struct HasBegin_Impl : std::false_type {};

template <typename T>
struct HasBegin_Impl<T, std::void_t<decltype(std::declval<T&>().begin())>> : std::true_type {};

template <typename T>
using HasBegin = HasBegin_Impl<T>;

template<typename T>
inline constexpr bool HasBegin_v = HasBegin<T>::value;
