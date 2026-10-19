# Review verdicts applied by merge_run

- comparing.more-than: route critic-route-1 removed (superset of another route); moved to related: nothing
- D14 shapes.closed-boundary -> spatial.position.relative: dropped
- shapes.closed-boundary: now a root (every prerequisite dropped or moved in review)
- A7 shapes.name.receptive -> shapes.match: dropped
- shapes.name.receptive: now a root (every prerequisite dropped or moved in review)
- cardinality.conservation: route critic-route-1 removed (superset of another route); moved to related: ['comparing.count.small-equal', 'counting.objects']
- A2, A9, D27, D28 cardinality.conservation: routes set to [('by-matching', ['comparing.count.matching:task', 'comparing.more-than:task']), ('by-counting', ['counting.objects:task', 'comparing.more-than:task']), ('by-small-equal', ['comparing.count.small-equal:task', 'comparing.more-than:task'])]; related []; dropped []
- fraction.compare.to-one: route critic-route-1 removed (superset of another route); moved to related: nothing
- fraction.compare.to-one: route critic-route-2 removed (superset of another route); moved to related: nothing
- D23 fraction.compare.to-one -> comparing.whole-numbers.symbols: replaced by comparing.whole-numbers.magnitude
- D24-D26 fraction.compare.to-one: routes set to [('as-b-over-b', ['comparing.whole-numbers.magnitude', 'fraction.whole-number.as-fraction', 'fraction.compare.same-denominator']), ('unit-fraction-count', ['comparing.whole-numbers.magnitude', 'fraction.multiple-of-unit'])]; related []; dropped []
- A8 division.facts.within-100 -> multiplication.facts.within-100: moved to related (common_path)
- D21 rational-number.negative-as-decrease -> rational-number.negative-meaning: dropped
- D22 rational-number.negative-as-decrease -> subtraction.whole-number: dropped
- rational-number.negative-as-decrease: now a root (every prerequisite dropped or moved in review)
