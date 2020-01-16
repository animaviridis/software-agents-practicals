at(0,0).

+!north : at(X0, Y0) <-
    .print("Moving north");
    -at(X0, Y0);
    +at(X0, Y0+1).

+!south <-
    .print("Moving south").


+!east : at(X0, Y0) <-
    .print("Moving east from ", X0, Y0);
    -at(X0, Y0);
    +at(X0+1, Y0);
    !print_location.

+!west <-
    .print("Moving west").


 !print_location.

 +!print_location:at(X,Y) <-
    .print("location is:", X,Y).


 +!move(X,Y):at(XO,YO)&X-XO>0 <-
    .print("X, Y: ", X, Y);
    .print("XO, YO: ", XO, YO);
    !east;
    +at(X+1,Y).

+!move(X,Y):at(XO,_)&X-XO<0 <-
    !west;
    +at(X+1,Y).

+!move(X,Y):at(_,YO)&Y-YO>0 <-
    !north;
    +at(X,Y+1).

+!move(X,Y):at(_,YO)&Y-YO<0 <-
    !south;
    +at(X,Y+1).

!move(3,4).
!print_location.