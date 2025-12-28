#include <vector>
#include <type_traits>
#include <string>

template <typename... Ts>
struct TypeList {};

template <size_t N, typename List>
struct GetTypeAtIndex {};

// Частичная специализация для рекурсивного шага
template <size_t N, typename H, typename... Ts>
struct GetTypeAtIndex<N, TypeList<H, Ts...>> {
    using type = typename GetTypeAtIndex<N - 1, TypeList<Ts...>>::type;
};

// Базовый случай рекурсии (когда N достигает 0)
template <typename H, typename... Ts>
struct GetTypeAtIndex<0, TypeList<H, Ts...>> {
    using type = H;
};

// Дополнительное задание: Concat - объединение двух TypeList
template <typename List1, typename List2>
struct Concat {};

template <typename... Ts1, typename... Ts2>
struct Concat<TypeList<Ts1...>, TypeList<Ts2...>> {
    using type = TypeList<Ts1..., Ts2...>;
};

// Дополнительное задание: RemoveAt - удаление элемента по индексу
template <size_t N, typename List>
struct RemoveAt {};

// Базовый случай: удаляем первый элемент (N = 0)
template <typename H, typename... Ts>
struct RemoveAt<0, TypeList<H, Ts...>> {
    using type = TypeList<Ts...>;
};

// Рекурсивный случай: сохраняем первый элемент и рекурсивно удаляем из хвоста
template <size_t N, typename H, typename... Ts>
struct RemoveAt<N, TypeList<H, Ts...>> {
    using type = typename Concat<
        TypeList<H>, 
        typename RemoveAt<N - 1, TypeList<Ts...>>::type
    >::type;
};
