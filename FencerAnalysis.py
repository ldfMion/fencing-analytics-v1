from action_provider import ActionProvider


class FencerAnalysis:
    def __init__(self, fencer_name: str, provider: ActionProvider):
        self.fencer_name = fencer_name
        self.provider = provider

    def get_attack_effectiveness(self):
        attacks_scored = self.provider.count_attacks_scored(self.fencer_name)
        counters_received = self.provider.count_counter_attacks_received(
            self.fencer_name
        )
        ripostes_received = self.provider.count_ripostes_received(self.fencer_name)
        return rounded(attacks_scored / (counters_received + ripostes_received))

    def get_defense_effectiveness(self):
        attacks_received = self.provider.count_attacks_received(self.fencer_name)
        counters_scored = self.provider.count_counter_attacks_scored(self.fencer_name)
        ripostes_scored = self.provider.count_ripostes_scored(self.fencer_name)
        return rounded((counters_scored + ripostes_scored) / attacks_received)

    def riposte_to_parry_ratio(self):
        """The number of parries that resulted in a scored riposte"""
        ripostes_scored = self.provider.count_ripostes_scored(self.fencer_name)
        failed_parries = self.provider.count_attacks_received_from_parries(
            self.fencer_name
        )
        return rounded(ripostes_scored / (ripostes_scored + failed_parries))

    def get_counter_attack_effectiveness(self):
        scored = self.provider.count_counter_attacks_scored(self.fencer_name)
        failed = self.provider.count_attacks_received_from_counter_attacks(
            self.fencer_name
        )
        return rounded(scored / (scored + failed))

    def get_action_distribution(self):
        counter_attacks = self.provider.count_counter_attacks_scored(
            self.fencer_name
        ) + self.provider.count_attacks_received_from_counter_attacks(self.fencer_name)
        attacks = (
            self.provider.count_attacks_scored(self.fencer_name)
            + self.provider.count_counter_attacks_received(self.fencer_name)
            + self.provider.count_ripostes_received(self.fencer_name)
        )
        parries = self.provider.count_ripostes_scored(
            self.fencer_name
        ) + self.provider.count_attacks_received_from_parries(self.fencer_name)
        total = counter_attacks + attacks + parries
        return {
            "C": rounded(counter_attacks / total),
            "A": rounded(attacks / total),
            "P": rounded(parries / total),
        }

    def get_received_distribution(self):
        counter_attacks = self.provider.count_counter_attacks_received(self.fencer_name)
        ripostes = self.provider.count_ripostes_received(self.fencer_name)
        attacks = self.provider.count_attacks_received(self.fencer_name)
        total = counter_attacks + attacks + ripostes
        return {
            "C": rounded(counter_attacks / total),
            "A": rounded(attacks / total),
            "R": rounded(ripostes / total),
        }

    def get_scored_distribution(self):
        counter_attacks = self.provider.count_counter_attacks_scored(self.fencer_name)
        ripostes = self.provider.count_ripostes_scored(self.fencer_name)
        attacks = self.provider.count_attacks_scored(self.fencer_name)
        total = counter_attacks + attacks + ripostes
        return {
            "C": rounded(counter_attacks / total),
            "A": rounded(attacks / total),
            "R": rounded(ripostes / total),
        }

    def get_aggression(self):
        """Offensive actions executed / defensive actions executed"""
        counter_attacks = self.provider.count_counter_attacks_scored(
            self.fencer_name
        ) + self.provider.count_attacks_received_from_counter_attacks(self.fencer_name)
        attacks = (
            self.provider.count_attacks_scored(self.fencer_name)
            + self.provider.count_counter_attacks_received(self.fencer_name)
            + self.provider.count_ripostes_received(self.fencer_name)
        )
        parries = self.provider.count_ripostes_scored(
            self.fencer_name
        ) + self.provider.count_attacks_received_from_parries(self.fencer_name)
        return rounded(attacks / (counter_attacks + parries))

    def attack_eff_against_counter_attack(self):
        counter_attacks_received = self.provider.count_counter_attacks_received(
            self.fencer_name
        )
        attacks_scored_on_counter_attacks = (
            self.provider.count_attacks_scored_on_counter_attacks(self.fencer_name)
        )
        return rounded(
            attacks_scored_on_counter_attacks
            / (counter_attacks_received + attacks_scored_on_counter_attacks)
        )

    def attack_eff_against_parry(self):
        ripostes_received = self.provider.count_ripostes_received(self.fencer_name)
        attacks_scored_on_ripostes = self.provider.count_attacks_scored_on_parries(
            self.fencer_name
        )
        return rounded(
            attacks_scored_on_ripostes
            / (attacks_scored_on_ripostes + ripostes_received)
        )

    def offense_ev(self):
        scored = self.provider.count_attacks_scored(self.fencer_name)
        received_while_attacking = self.provider.count_counter_attacks_received(
            self.fencer_name
        ) + self.provider.count_ripostes_received(self.fencer_name)
        total = scored + received_while_attacking
        return rounded(scored / total - received_while_attacking / total)

    def defense_ev(self):
        scored = self.provider.count_counter_attacks_scored(
            self.fencer_name
        ) + self.provider.count_ripostes_scored(self.fencer_name)
        received_while_defending = self.provider.count_attacks_received(
            self.fencer_name
        )
        total = scored + received_while_defending
        return rounded(scored / total - received_while_defending / total)

    def __str__(self):
        action_dist = self.get_action_distribution()
        scored_dist = self.get_scored_distribution()
        received_dist = self.get_received_distribution()
        return (
            f"Analyzing: {self.fencer_name}\n"
            + "\n=== Fencer Performance Summary ===\n"
            + (f"Attack Effectiveness:        {self.get_attack_effectiveness():.2f}\n")
            + (f"Defense Effectiveness:       {self.get_defense_effectiveness():.2f}\n")
            + (f"Aggression:                  {self.get_aggression()}\n")
            + (f"Riposte to parry ratio:         {self.riposte_to_parry_ratio():.2f}\n")
            + (
                f"Counter-Attack Effectiveness:{self.get_counter_attack_effectiveness():.2f}\n"
            )
            + (
                f"Attacks scored on counter-attacks: {self.attack_eff_against_counter_attack()}\n"
            )
            + (f"Attacks scored on parries: {self.attack_eff_against_parry()}\n")
            + (f"Expected value of offense: {self.offense_ev()}\n")
            + (f"Expected value of defense: {self.defense_ev()}\n")
            + ("Action Distribution:\n")
            + (f"Attack: {action_dist['A']}\n")
            + (f"Counter-attack: {action_dist['C']}\n")
            + (f"Parry: {action_dist['P']}\n")
            + ("Scored Touches Distribution\n")
            + (f"Attack: {scored_dist['A']}\n")
            + (f"Counter-attack: {scored_dist['C']}\n")
            + (f"Ripostes: {scored_dist['R']}\n")
            + ("Received Touches Distribution\n")
            + (f"Attack: {received_dist['A']}\n")
            + (f"Counter-attack: {received_dist['C']}\n")
            + (f"Ripostes: {received_dist['R']}\n")
            + ("=" * 36)
            + "\n"
        )


def rounded(num: float):
    return round(num, 2)
