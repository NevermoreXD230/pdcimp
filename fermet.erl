-module(fermat).
-export([is_prime/1]).

is_prime(N) ->
    RandomNum = rand:uniform(N-2) + 1,
    fermat_test(N, RandomNum, 5).

fermat_test(_, _, 0) ->
    true;
fermat_test(N, A, TriesLeft) ->
    case exp_modulo(A, N-1, N) == 1 of
        true -> fermat_test(N, rand:uniform(N-2) + 1, TriesLeft-1);
        false -> false
    end.

exp_modulo(_, 0, _)-> 1;
exp_modulo(X, Y, M) when Y rem 2 =:= 0 ->
    Z = exp_modulo(X, Y div 2, M),
    (Z * Z) rem M;
exp_modulo(X, Y, M) ->
    (X * exp_modulo(X, Y-1, M)) rem M.
