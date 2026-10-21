# Merges after the writers (Claude, script pass, 2026-10-21)

Found by an id and text-similarity scan across the phase 3 skeletons and the
written map. Siblings written from one template (the same sentence for another
operation, range or sign) were left alone. Daniel's to reverse: phase 1 merged
two range variants that later had to be split back (F97).

- coordinate-plane.distance.same-coordinate (Q1, 6.NS.C.8) dropped: its test has
  two problem types (opposite signs, same sign), which are exactly G3's
  coordinate-plane.segment-length.opposite-sign and .same-sign (6.G.A.3, split by
  the range rule: adding versus subtracting absolute values). Its component
  1ba53b4c is now cited by both.
- coordinate-plane.application.mathematical.four-quadrants (Q1, 6.NS.C.8) merged
  into coordinate-plane.polygon.missing-vertex (G3, 6.G.A.3): the same problem
  (three vertices of an axis-parallel rectangle, find the fourth), one by
  plotting and one by coordinates. One node, stated method-neutrally; plotting
  and the shared-coordinate rule become routes. Cites both components.
- rational-number.compute.properties-strategy (E1, 7.EE.B.3) dropped: same test as
  Q1's rational-number.multiplication.properties-strategy (4 x (-3.7) x 25 versus
  -4 x 2.7 x (-25)); Q1 split the strategy by operation. Component 35c2f57a
  stays cited by E1's rational-number.compute.mixed-forms.

Kept apart: the real-world and mathematical versions of the same task
(rational-number.application.multistep.*, coordinate-plane.application.*):
the writers split them by problem class, and whether context changes the
prerequisites is review item 3 (application scope) for Daniel.
