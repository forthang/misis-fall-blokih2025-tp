#include <iostream>
#include <tuple>
#include <string>
#include <utility>

// --- РЕАЛИЗАЦИЯ ЗАДАЧИ ---

// 1. Вспомогательная функция, которая принимает последовательность индексов.
template <typename Tuple, typename Func, std::size_t... Is>
void for_each_in_tuple_impl(Tuple&& t, Func&& f, std::index_sequence<Is...>) {
    // Выражение свёртки C++17 с оператором запятая
    ((void)std::forward<Func>(f)(std::get<Is>(std::forward<Tuple>(t))), ...);
}

// 2. Основной публичный интерфейс
template <typename Tuple, typename Func>
void for_each_in_tuple(Tuple&& t, Func&& f) {
    constexpr std::size_t N = std::tuple_size_v<std::decay_t<Tuple>>;
    for_each_in_tuple_impl(
        std::forward<Tuple>(t),
        std::forward<Func>(f),
        std::make_index_sequence<N>{}
    );
}

// --- ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ ---

// Вспомогательная функция для tuple_transform
template <typename Tuple, typename Func, std::size_t... Is>
auto tuple_transform_impl(Tuple&& t, Func&& f, std::index_sequence<Is...>) {
    // Выражение свёртки для создания нового кортежа
    return std::make_tuple(std::forward<Func>(f)(std::get<Is>(std::forward<Tuple>(t)))...);
}

// Основная функция tuple_transform
template <typename Tuple, typename Func>
auto tuple_transform(Tuple&& t, Func&& f) {
    constexpr std::size_t N = std::tuple_size_v<std::decay_t<Tuple>>;
    return tuple_transform_impl(
        std::forward<Tuple>(t),
        std::forward<Func>(f),
        std::make_index_sequence<N>{}
    );
}
