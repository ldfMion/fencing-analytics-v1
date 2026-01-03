# Fencing Analysis

This project analyzes fencing data from a CSV file and calculates various metrics.

# issues
- ripostes and counter ripostes are always defensive, but that doesn't make sense because then both fencers would be doing a defensive action at the same time (but in a simultaneous attack both would be doing an offensive action but that does make sense)
- failed defense with distance is classified as an attack, since it corresponds to an answering attack, but a successful defense with distance doesn't necessarily lead to a answering attack
- If I try to parry a riposte, it should still be classified as offensive and should it still be attack? I don't think this is handled
- Missing line (Cl) in the dictionary
- Renewals of answering attacks count the same as regular attack renewals, which shouldn't be the case since answering attack is a defensive action
- back line and cards don't count in the analysis of actions, but should count in things like score differential, etc

# actions grammar

<action> ::= <action-type> | <action>r
<action-type> ::= <attack> | <counter-attack> | <riposte>
<attack> ::= A<attack-suffix> | A
<attack-suffix> ::=  p | f | bt
<counter-attack> ::= C<counter-attack-suffix>
<counter-attack-suffix> ::= sh | c | l | d | l
<riposte> ::= R | c<riposte>
