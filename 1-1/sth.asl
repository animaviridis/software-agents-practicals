!dosomething.

b([1,2,3,4]).

+!dosomething : b([H|T]) <-
    .print(H);
    -b([H|T]);
    +b(T);
    !dosomething.

+!dosomething : b([]) <-
    .print("finished").
