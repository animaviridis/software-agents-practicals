garbageAt([5, 1]).
currentPos([3, 4]).

!start.

+!start <-
    !ask_for_coordinates.


+!ask_for_coordinates <-
    .print("Asking for garbage coordinates...");
    .send(garbage_sensor, achieve, receive_query("Location please"));
    .print("Query sent").


+!receive_coordinates(XY_new)[source(Sender)] : garbageAt(XY) <-
    .print("Received garbage coordinates: ", XY_new);
    +garbageAt(XY_new);
    -garbageAt(XY);
    !process_coordinates.

+!process_coordinates: garbageAt([X, Y]) <-
    +garbageOnFloor;
    !move.

+!process_coordinates: garbageAt([]) <-
    .print("All cleaned up").


+!move : garbageAt([A, B]) & currentPos([X, Y]) & X < A <-
    !printPositions;
    .print("Going North");
    +currentPos([X+1, Y]);
    -currentPos([X, Y]);
    !move.


+!move : garbageAt([A, B]) & currentPos([X, Y]) & X > A <-
    !printPositions;
    .print("Going South");
    +currentPos([X-1, Y]);
    -currentPos([X, Y]);
    !move.


+!move : garbageAt([A, B]) & currentPos([X, Y]) & Y > B <-
    !printPositions;
    .print("Going East");
    +currentPos([X, Y-1]);
    -currentPos([X, Y]);
    !move.


+!move : garbageAt([A, B]) & currentPos([X, Y]) & Y < B <-
    !printPositions;
    .print("Going West");
    +currentPos([X, Y+1]);
    -currentPos([X, Y]);
    !move.


+!move : garbageAt([A, B]) & currentPos([X, Y]) <-
    !printPositions;
    !pickup.


+!printPositions : garbageAt(AB) & currentPos(XY) <-
    .print("My position: ", XY, ", garbage position: ", AB).


+!pickup : .random(S) & S<0.5 <-
    -garbageOnFloor;
    +garbageInHand;
    .print("Picked up");
    !ask_for_coordinates.


+!pickup : garbageOnFloor <-
    .print("Attempted pick up");
    !pickup.
