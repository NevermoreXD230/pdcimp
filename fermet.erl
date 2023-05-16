-module(fermet).
-export([is_prime/1]).

is_prime(N) ->
    is_prime(N, 20).

is_prime(_, 0) -> true;
is_prime(N, K) ->
    A = rand:uniform(N - 2) + 1,
    case fermat_test(A, N) of
        true ->
            is_prime(N, K - 1);
        false ->
            false
    end.

fermat_test(A, N) ->
    case expmod(A, N-1, N) of
        1 -> true;
        _ -> false
    end.

expmod(_, 0, N) -> 1;
expmod(B, E, N) when E rem 2 == 0 ->
    ((expmod(B, E div 2, N)) rem N) * ((expmod(B, E div 2, N)) rem N) rem N;
expmod(B, E, N) ->
    ((B rem N) * (expmod(B, E - 1, N) rem N)) rem N.
