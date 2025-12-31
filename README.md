# Fencing Analysis

This project analyzes fencing data from a CSV file and calculates various metrics.

# issues
- ripostes and counter ripostes are always defensive, but that doesn't make sense because then both fencers would be doing a defensive action at the same time (but in a simultaneous attack both would be doing an offensive action but that does make sense)
- failed defense with distance is classified as an attack, since it corresponds to an answering attack, but a successful defense with distance doesn't necessarily lead to a answering attack

# actions grammar

<action> ::= <action-type> | <action>r
<action-type> ::= <attack> | <counter-attack> | <riposte>
<attack> ::= A<attack-suffix> | A
<attack-suffix> ::=  p | f | bt
<counter-attack> ::= C<counter-attack-suffix>
<counter-attack-suffix> ::= sh | c | l | d
<riposte> ::= R | c<riposte>
