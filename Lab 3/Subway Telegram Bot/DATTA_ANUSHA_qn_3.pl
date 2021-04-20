/* Facts (Predicate with Terms) */
healthy_meal(healthy).
value_meal(value).
vegan_meal(vegan).
veggie_meal(veggie).
meaty_delight_meal(meaty_delight).

/* Data Collection */
all_options(A, X):-
    A == meals -> meals(X);
    A == breads -> breads(X);
    A == mains -> mains(X);
    A == veggies -> veggies(X);
    A == sauces -> sauces(X);
    A == topups -> topups(X);
    A == sides -> sides(X);
    A == drinks -> drinks(X).

/* Data Collection for available options */
available_options(A, X):-
    A == meals -> ask_meals(X);
    A == breads -> ask_breads(X);
    A == mains -> ask_mains(X);
    A == veggies -> ask_veggies(X);
    A == sauces -> ask_sauces(X);
    A == topups -> ask_topups(X);
    A == sides -> ask_sides(X);
    A == drinks -> ask_drinks(X).

/* Data Collection based on user inputs */
selected_options(A, X):-
    A == meals -> findall(X, selected_meals(X), X);
    A == breads -> findall(X, selected_breads(X), X);
    A == mains -> findall(X, selected_mains(X), X);
    A == veggies -> findall(X, selected_veggies(X), X);
    A == sauces -> findall(X, selected_sauces(X), X);
    A == topups -> findall(X, selected_topups(X), X);
    A == sides -> findall(X, selected_sides(X), X);
    A == drinks -> findall(X, selected_drinks(X), X).


/* 

Enumerating each option 

*/

meals([normal, value, veggie, meaty_delight, healthy, vegan]).

/* Value/Expensive Mains */
value_mains([egg_mayonnaise, chicken, tuna, ham]).
expensive_mains([beef, salmon]).

/* Breads */
vegan_breads([hearty_italian, multigrain, flatbread, italian_wheat, parmesan_oregano]).
non_vegan_breads([honey_oat]).

/* Sauces */
healthy_sauces([sweet_onion, honey_mustard, chilli]).
unhealthy_sauces([ranch, mayonnaise, chipotle_southwest, bbq]).

/* Veggies */
veggies([lettuce, micro_greens, corn, beetroot, carrot, cucumber, green_peppers, onions, tomatoes, olives, jalapenos, pickles]).

/* Top Ups */
non_vegan_topups([cheddar_cheese, mozzarella_cheese]).
vegan_topups([avocado, toasted_mushrooms]).

/* Sides */
healthy_sides([energy_bar, energy_drink]).
unhealthy_sides([cookies, chips]).

/* Drinks */
healthy_drinks([mineral_water, orange_juice]).
unhealthy_drinks([fountain_drinks, sprite, coca_cola]).

/* Return breads list */
breads(X):-
    vegan_breads(B1), non_vegan_breads(B2), append(B1, B2, X).


/* Return mains list */
mains(X):-
    value_mains(M1), expensive_mains(M2), append(M1, M2, X).


/* Return sauces list */
sauces(X):-
    healthy_sauces(S1), unhealthy_sauces(S2), append(S1, S2, X).


/* Return add ons list */
topups(X):-
    non_vegan_topups(T1), vegan_topups(T2), append(T1, T2, X).


/* Return sides list */
sides(X):-
    healthy_sides(S1), unhealthy_sides(S2), append(S1, S2, X).


/* Return drinks list */
drinks(X):-
    healthy_drinks(D1), unhealthy_drinks(D2), append(D1, D2, X).

    
/* Return meals list based on user selections */
ask_meals(X):-
    meals(X).


/* Return possible breads based on user selections */
/* Vegan Bread will exclude Honey Oat */
ask_breads(X):-
    selected_meals(Y), vegan_meal(Y) -> vegan_breads(X);   
    breads(X).

/* Return possible mains based on user selections */
/* Value meals exclude expensive mains */
/* Vegan & Veggie meals exclude all mains, return empty list []. */
ask_mains(X):-
    selected_meals(Y), vegan_meal(Y) -> empty_list(X);
    selected_meals(Y), veggie_meal(Y) -> empty_list(X);
    selected_meals(Y), value_meal(Y) -> value_mains(X); 
    mains(X).


/* Return possible veggies based on user selections */
/* Meaty delight meals exclude veggie options, return empty list []. */
ask_veggies(X):-
    selected_meals(Y), \+ meaty_delight_meal(Y), veggies(X).


/* Return possible sauces based on user selections */
/* Healthy meals exclude unhealthy sauces */
ask_sauces(X):-
    selected_meals(Y), healthy_meal(Y) -> healthy_sauces(X);   
    sauces(X).


/* Return a list of possible top-ups based on previous choices */
/* Value meal has NO topup, returns an empty list [] */
/* Vegan meal only includes vegan topups */
ask_topups(X):-
    selected_meals(Y), value_meal(Y) -> empty_list(X);
    selected_meals(Y), vegan_meal(Y) -> vegan_topups(X); 
    topups(X).


/* Return possible sides based on user selections */
/* Healthy meals excludes unhealthy sides */
ask_sides(X):-
    selected_meals(Y), healthy_meal(Y) -> healthy_sides(X);   
    sides(X).


/* Return possible drinks based on user selections */
/* Healthy meals excludes unhealthy drinks */
ask_drinks(X):-
    selected_meals(Y), healthy_meal(Y) -> healthy_drinks(X);   
    drinks(X).

/* Helper List Function */
append([], Y, Y).
append([H|X], Y, [H|Z]):-
    append(X, Y, Z).


/* Empty list variable */
empty_list([]).