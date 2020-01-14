garbageOnFloor.

!pickup.

+!pickup : .random(X) & X<0.5 <-
-garbageOnFloor;
+garbageInHand.

+!pickup : garbageOnFloor <-
.print("Picking up");
!pickup.