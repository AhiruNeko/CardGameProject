import random as rd


class Card:

    def __init__(self, **kwargs):
        self.name = "card"
        self.value = 0

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name if isinstance(other, Card) else False

    def __hash__(self):
        return self.name.__hash__()

    def execute(self, *players):
        pass


class Basic_Card(Card):

    def __init__(self, player, **kwargs):
        super().__init__()
        self.player = player
        self.type = kwargs["type"]


class Normal_Card(Basic_Card):

    def __init__(self, player, **kwargs):
        super().__init__(player, **kwargs)
        self.player = player

        self.range: str = kwargs["range"]  # "air" "land"
        # self.type: str = kwargs["type"]  # "def" "atk"
        self.name = " ".join([kwargs["type"], kwargs["range"], "card"])
        try:
            self.level: int = kwargs["level"]  # 1(low) 2(high)
            self.name = " ".join([kwargs["type"], str(kwargs["level"]), kwargs["range"], "card"])
        except KeyError:
            pass

        if self.type == "def":
            self.value = self.level
        elif self.type == "atk":
            self.value = -2

    def execute(self):
        if self.type == "def":
            self.player.hp += self.value
        elif self.type == "atk":
            self.player.enemy.hp += self.value


class Skill_Card(Basic_Card):
    """
    comprehensive_def, impeccable, first_aid, fierce_attack
    """

    def __init__(self, player, **kwargs):
        super().__init__(player, **kwargs)
        self.life = 2
        self.name = self.type + " card"

    def __str__(self):
        return self.name + " " + str(self.life)


class Judgement_Card(Card):

    def __init__(self):
        super().__init__()
        self.probability = 0.5

    def update(self, counter):
        if counter < 5:
            self.probability = 0.2
        elif counter < 10:
            self.probability = 0.5
        else:
            self.probability = 0.8


class Lightning_Card(Judgement_Card):

    def __init__(self):
        super().__init__()
        self.type = "lightning"
        self.name = " ".join([self.type, "card"])
        self.value = -1

    def execute(self, *players):
        if rd.random() < self.probability:
            for p in players:
                if p.skill is not None and p.skill.type == "impeccable":
                    p.skill = None
                    return False
            player = rd.choice(players)
            player.hp += self.value
            return player.name
        return False

    def update(self, counter):
        if counter < 5:
            self.probability = 0.5
        else:
            self.probability = 1


class Airstrike_Card(Judgement_Card):

    def __init__(self):
        super().__init__()
        self.type = "airstrike"
        self.name = " ".join([self.type, "card"])
        self.value = -1

    def execute(self, *players) -> bool:
        if rd.random() < self.probability:
            for p in players:
                if p.skill is not None and p.skill.type == "impeccable":
                    p.skill = None
                    return False
            for p in players:
                p.hp += self.value
            return True
        return False


class Restore_Card(Judgement_Card):

    def __init__(self):
        super().__init__()
        self.type = "restore"
        self.name = " ".join([self.type, "card"])
        self.value = 1

    def execute(self, *players) -> bool:
        if rd.random() < self.probability:
            for p in players:
                if p.skill is not None and p.skill.type == "impeccable":
                    p.skill = None
                    return False
            for p in players:
                p.hp += self.value
            return True
        return False

    def update(self, counter):
        if counter < 5:
            self.probability = 0.8
        elif counter < 10:
            self.probability = 0.5
        else:
            self.probability = 0.1


class Famine_Card(Judgement_Card):

    def __init__(self):
        super().__init__()
        self.type = "famine"
        self.name = " ".join([self.type, "card"])

    def execute(self, *players) -> bool:
        if rd.random() < self.probability:
            for p in players:
                if p.skill is not None and p.skill.type == "impeccable":
                    p.skill = None
                    return False
            for p in players:
                if p.cards:
                    card_index = rd.randint(0, len(p.cards) - 1)
                    p.cards.pop(card_index)
            return True
        return False


class Player:

    def __init__(self, name="player"):
        self.name = name
        self.hp_max = 5
        self.hp = self.hp_max
        self.cards_max = 4
        self.cards = []
        self.skill = None
        self.enemy = None

    def __str__(self):
        return self.name

    def set_enemy(self, enemy):
        self.enemy = enemy

    def play_card(self, card_index):
        return self.cards.pop(card_index)

    def get_basic_cards(self, num):
        for i in range(num):
            random_num = rd.random()
            if random_num < 0.6:
                rd_num = rd.random()
                if rd_num < 0.25:
                    self.cards.append(Normal_Card(self, type="atk", range="air"))
                elif rd_num < 0.5:
                    self.cards.append(Normal_Card(self, type="atk", range="land"))
                elif rd_num < 0.625:
                    self.cards.append(Normal_Card(self, type="def", level=1, range="air"))
                elif rd_num < 0.75:
                    self.cards.append(Normal_Card(self, type="def", level=2, range="air"))
                elif rd_num < 0.875:
                    self.cards.append(Normal_Card(self, type="def", level=1, range="land"))
                else:
                    self.cards.append(Normal_Card(self, type="def", level=2, range="land"))
            else:
                self.cards.append(rd.choice([Skill_Card(self, type="comprehensive_def"), Skill_Card(self, type="first_aid"),
                                             Skill_Card(self, type="impeccable"), Skill_Card(self, type="fierce_attack")]))

    def fold(self, card_index):
        try:
            self.cards.pop(card_index)
        except IndexError:
            pass

    def is_full(self) -> bool:
        return len(self.cards) > self.cards_max

    def update_hp(self):
        self.hp = min(self.hp, self.hp_max)
        if 0 >= self.hp == self.enemy.hp <= 0:
            self.hp = 1
            self.enemy.hp = 1

    def get_skill_cards(self) -> list:
        return [i for i in self.cards if isinstance(i, Skill_Card)]

    def get_normal_cards_index(self):
        return [i for i in range(len(self.cards)) if isinstance(self.cards[i], Normal_Card)]


class Round:

    def __init__(self):
        self.player1 = Player("p1")
        self.player2 = Player("p2")
        self.player1.set_enemy(self.player2)
        self.player2.set_enemy(self.player1)
        self.players = [self.player1, self.player2]
        for p in self.players:
            p.get_basic_cards(2)
        self.counter = 0

    @staticmethod
    def get_judgement_card() -> Judgement_Card:
        return rd.choice([Airstrike_Card(), Famine_Card(), Lightning_Card(), Restore_Card()])

    def run_c2c(self, log=True) -> tuple:

        while True:
            self.counter += 1
            mechanism = False

            for p in self.players:
                p.get_basic_cards(2)
                if p.is_full():
                    p.fold(rd.randint(0, len(p.cards) - 1))

            if log:
                print("\np1: " + str([str(i) for i in self.player1.cards]) + " | " + str(
                    self.player1.skill) + " | " + str(self.player1.hp))
                print("\np2: " + str([str(i) for i in self.player2.cards]) + " | " + str(
                    self.player2.skill) + " | " + str(self.player2.hp))
                print("\n")

            for p in self.players:
                skill_cards = p.get_skill_cards()
                if skill_cards and rd.random() < 0.5:
                    p.skill = rd.choice(skill_cards)
                    p.cards.remove(p.skill)

            if log:
                print("\np1: " + str([str(i) for i in self.player1.cards]) + " | " + str(
                    self.player1.skill) + " | " + str(self.player1.hp))
                print("\np2: " + str([str(i) for i in self.player2.cards]) + " | " + str(
                    self.player2.skill) + " | " + str(self.player2.hp))
                print("\n")

            if not (self.player1.get_normal_cards_index() == [] or self.player2.get_normal_cards_index()== []):
                rd1 = rd.choice(self.player1.get_normal_cards_index())
                rd2 = rd.choice(self.player2.get_normal_cards_index())
                card1: Normal_Card = self.player1.play_card(rd1)
                card2: Normal_Card = self.player2.play_card(rd2)

                if card1.type == "def" and card2.type == "atk" and card1.range == card2.range:
                    if self.player1.skill is not None and self.player1.skill.type == "comprehensive_def":
                        self.player1.skill = None
                    else:
                        card2.execute()
                        card1.execute()
                elif card1.type == "atk" and card2.type == "def" and card1.range == card2.range:
                    if self.player2.skill is not None and self.player2.skill.type == "comprehensive_def":
                        self.player2.skill = None
                    else:
                        card2.execute()
                        card1.execute()
                elif card1.type == "atk" and card2.type == "atk":
                    if (self.player1.skill is None or self.player1.skill.type != "fierce_attack") and (self.player2.skill is None or self.player2.skill.type != "fierce_attack"):
                        card1.execute()
                        card2.execute()
                    for p in self.players:
                        if p.skill is not None and p.skill.type == "fierce_attack":
                            p.enemy.hp -= 1
                            p.skill = None
                elif card1.type == "def" and card2.type == "atk" and card1.range != card2.range:
                    if self.player1.skill is not None and self.player1.skill.type == "comprehensive_def":
                        self.player1.skill = None
                    else:
                        card2.execute()
                        if rd.random() < 0.5:
                            card1.player.hp += 1
                            mechanism = True
                elif card1.type == "atk" and card2.type == "def" and card1.range != card2.range:
                    if self.player2.skill is not None and self.player2.skill.type == "comprehensive_def":
                        self.player2.skill = None
                    else:
                        card1.execute()
                        if rd.random() < 0.5:
                            card2.player.hp += 1
                            mechanism = True
                elif card1.type == "def" and card2.type == "def":
                    if rd.random() < 0.5:
                        for p in self.players:
                            p.hp += 1
                        mechanism = True
            elif self.player1.get_normal_cards_index() != [] and self.player2.get_normal_cards_index() == []:
                rd1 = rd.choice(self.player1.get_normal_cards_index())
                card1: Normal_Card = self.player1.play_card(rd1)
                card2 = "skip"
                if card1.type == "atk":
                    card1.execute()
            elif self.player1.get_normal_cards_index() == [] and self.player2.get_normal_cards_index() != []:
                rd2 = rd.choice(self.player2.get_normal_cards_index())
                card1 = "skip"
                card2: Normal_Card = self.player2.play_card(rd2)
                if card2.type == "atk":
                    card2.execute()
            else:
                card1 = "skip"
                card2 = "skip"

            j_card = self.get_judgement_card()
            j_card.update(self.counter)
            j_result = j_card.execute(self.player1, self.player2)

            for p in self.players:
                p.update_hp()
                if p.skill is not None and p.skill.type == "first_aid" and p.hp <= 0:
                    p.hp = 1
                    p.skill = None

            for p in self.players:
                if p.skill is not None:
                    p.skill.life -= 1
                    if p.skill.life == 0:
                        p.skill = None

            if log:
                print("\np1: " + str([str(i) for i in self.player1.cards]) + " | " + str(self.player1.skill) + " | " + str(card1) + " | " + str(self.player1.hp))
                print("\np2: " + str([str(i) for i in self.player2.cards]) + " | " + str(self.player2.skill) + " | " + str(card2) + " | " + str(self.player2.hp))
                print("\n" + str(j_card) + " -> " + str(j_result))
                print("\nmechanism -> " + str(mechanism))
                print("-----------------------------------------------------------------------------------------------")

            if self.player1.hp <= 0 and self.player1.hp < self.player2.hp:
                print("\n\n===========================================================================================")
                print("p2 win.")
                print("Total round:", self.counter)
                return "p2", self.counter
            elif self.player2.hp <= 0 and self.player2.hp < self.player1.hp:
                print("\n\n===========================================================================================")
                print("p1 win.")
                print("Total round:", self.counter)
                return "p1", self.counter


def main1():
    p1_counter = 0
    p2_counter = 0
    round_counter = 0
    n = 10000
    for i in range(n):
        round_test = Round()
        winner, rounds = round_test.run_c2c(False)
        p1_counter += 1 if winner == "p1" else 0
        p2_counter += 1 if winner == "p2" else 0
        round_counter += rounds
    print("\n\n")
    print("p1 win:", p1_counter / n)
    print("p2 win:", p2_counter / n)
    print("average round:", round_counter / n)


def main2():
    round_test = Round()
    round_test.run_c2c()


def main3():
    round_counter = []
    n = 1000
    for i in range(n):
        round_test = Round()
        rounds = round_test.run_c2c(False)[1]
        round_counter.append(rounds)
    round_dict = dict()
    for i in round_counter:
        if i in round_dict:
            round_dict[i] += 1
        else:
            round_dict[i] = 1
    x = list(round_dict.keys())
    x.sort()
    y = [round_dict[i] for i in x]
    print(sum(round_counter) / n)

    import matplotlib.pyplot as plt
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    main2()

