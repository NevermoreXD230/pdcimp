-module(worker).
-export([calculate_primes/2]).

calculate_primes(Start, End) ->
    [ N || N <- lists:seq(Start, End), is_prime(N) ].

is_prime(N) ->
    case fermet(N) of
        true -> true;
        false -> false
    end.

fermet(N) ->
    A = random:uniform(N-1) + 1,
    A == fast_exp(A, N-1, N).

fast_exp(_, 0, _) ->
    1;
fast_exp(Base, Exponent, Mod) ->
    case Exponent rem 2 of
        0 ->
            Result = fast_exp(Base, Exponent div 2, Mod),
            (Result * Result) rem Mod;
        1 ->
            (Base * fast_exp(Base, Exponent - 1, Mod)) rem Mod
    end.
