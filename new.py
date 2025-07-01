import random as rd


class Card:

    def __init__(self, **kwargs):
        self.name = "card"
        self.value = 0

    def __str__(self):
        return self.name

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

    def execute(self, random_num):
        if self.type == "def" and self.player.enemy.card.type == "atk" and self.range == self.player.enemy.card.range:
            if self.player.skill.type == "comprehensive_def":
                self.player.hp += 2
                self.player.skill.life = 0
            else:
                self.player.hp += self.value
        elif self.type == "def" and self.player.enemy.card.type == "atk" and self.range != self.player.enemy.card.range:
            if self.player.skill.type == "comprehensive_def":
                self.player.hp += 2
                self.player.skill.life = 0
            elif rd.random() < 0.5:
                self.player.hp += 1
                return True
        elif self.type == "atk" and self.player.enemy.card.type != "atk":
            self.player.enemy.hp += self.value
        elif self.type == self.player.enemy.card.type == "atk":
            if self.player.skill.type == "fierce_attack" and self.player.enemy.skill.type != "fierce_attack":
                self.player.enemy.hp -= 1
                self.player.skill.life = 0
            elif self.player.skill.type != "fierce_attack" and self.player.enemy.skill.type != "fierce_attack":
                self.player.enemy.hp += self.value
            elif self.player.skill.type == "fierce_attack" and self.player.enemy.skill.type == "fierce_attack":
                self.player.enemy.hp -= 1
                self.player.skill.life = 0
        elif self.type == self.player.enemy.card.type == "def":
            if random_num < 0.5:
                self.player.hp += 1
                return True
        return False


class Skill_Card(Basic_Card):
    """
    comprehensive_def, impeccable, first_aid, fierce_attack, none
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
                if p.skill.type == "impeccable":
                    p.skill.life = 0
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
                if p.skill.type == "impeccable":
                    p.skill.life = 0
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
                if p.skill.type == "impeccable":
                    p.skill.life = 0
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
                if p.skill.type == "impeccable":
                    p.skill.life = 0
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
        self.skill = Skill_Card(self, type="none")
        self.enemy = None
        self.card = Normal_Card(self, type="none", range="")

    def __str__(self):
        return self.name

    def set_enemy(self, enemy):
        self.enemy = enemy

    def play_card(self, card_index):
        self.card = self.cards.pop(card_index)

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
                self.cards.append(rd.choice([Skill_Card(self, type="comprehensive_def"),
                                             Skill_Card(self, type="first_aid"),
                                             Skill_Card(self, type="impeccable"),
                                             Skill_Card(self, type="fierce_attack")]))

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

    def skip(self):
        self.card = Normal_Card(self, type="skip", range="")


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

    def run(self, mode="c2c", log=1) -> tuple:
        """
        mode:
          "c2c": computer versus computer
            self.player1: computer
            self.player2: computer
          "c2p": computer versus player
            self.player1: computer
            self.player2: player
          "p2p": player versus player
            self.player1: player
            self.player2: player
        log:
          0: no log
          1: detailed log
          2: simple log
        """
        first_round = True
        while True:
            self.counter += 1

            # Draw cards and fold
            if mode == "c2c":
                for p in self.players:
                    p.get_basic_cards(2)
                    while p.is_full():
                        p.fold(rd.randint(0, len(p.cards) - 1))
            elif mode == "p2p":
                for p in self.players:
                    p.get_basic_cards(2)
                    while True:
                        try:
                            p.fold(int(input("Please fold: " + str([str(i) for i in p.cards]))))
                            if p.is_full():
                                continue
                            else:
                                break
                        except Exception:
                            continue
            elif mode == "c2p":
                for p in self.players:
                    p.get_basic_cards(2)
                while self.player1.is_full():
                    self.player1.fold(rd.randint(0, len(self.player1.cards) - 1))
                while True:
                    try:
                        self.player2.fold(int(input("Please fold: " + str([str(i) for i in self.player2.cards]))))
                        if self.player2.is_full():
                            continue
                        else:
                            break
                    except Exception:
                        continue

            if log == 1:
                print("\nDraw cards:")
                print("\np1: " + str([str(i) for i in self.player1.cards]) + " | Skill: " + str(
                    self.player1.skill) + " | HP: " + str(self.player1.hp))
                print("\np2: " + str([str(i) for i in self.player2.cards]) + " | Skill: " + str(
                    self.player2.skill) + " | HP: " + str(self.player2.hp))
                print("\n")

            # Equip skills
            if mode == "c2c":
                for p in self.players:
                    skill_cards = p.get_skill_cards()
                    if skill_cards and rd.random() < 0.5:
                        p.skill = rd.choice(skill_cards)
                        p.cards.remove(p.skill)
            elif mode == "p2p":
                for p in self.players:
                    skill_cards = p.get_skill_cards()
                    while True:
                        user_input = input("Equip your skill: " + str([str(i) for i in skill_cards]))
                        if user_input != "none":
                            try:
                                p.skill = skill_cards[int(user_input)]
                            except Exception:
                                continue
                            p.cards.remove(p.skill)
                            break
                        elif user_input == "none":
                            break
            elif mode == "c2p":
                skill_cards = self.player1.get_skill_cards()
                if skill_cards and rd.random() < 0.5:
                    self.player1.skill = rd.choice(skill_cards)
                    self.player1.cards.remove(self.player1.skill)

                skill_cards = self.player2.get_skill_cards()
                while True:
                    user_input = input("Equip your skill: " + str([str(i) for i in skill_cards]))
                    if user_input != "none":
                        try:
                            p.skill = skill_cards[int(user_input)]
                        except Exception:
                            continue
                        p.cards.remove(p.skill)
                        break
                    elif user_input == "none":
                        break

            if log == 1:
                print("Equip skills:")
                print("\np1: " + str([str(i) for i in self.player1.cards]) + " | Skill: " + str(
                    self.player1.skill) + " | HP: " + str(self.player1.hp))
                print("\np2: " + str([str(i) for i in self.player2.cards]) + " | Skill: " + str(
                    self.player2.skill) + " | HP: " + str(self.player2.hp))
                print("\n")

            # Play cards
            # Player1
            if not (self.player1.get_normal_cards_index() == []):
                if mode == "c2c" or mode == "c2p":
                    index1 = rd.choice(self.player1.get_normal_cards_index())
                    self.player1.play_card(index1)
                elif mode == "p2p":
                    while True:
                        try:
                            index1 = int(input("Play your cards: " + str([str(i) for i in self.player1.cards])))
                            if isinstance(self.player1.cards[index1], Normal_Card):
                                break
                        except Exception:
                            continue
                    self.player1.play_card(index1)
            else:
                self.player1.skip()

            # Player2
            if not (self.player2.get_normal_cards_index() == []):
                if mode == "c2c":
                    index2 = rd.choice(self.player2.get_normal_cards_index())
                    self.player2.play_card(index2)
                elif mode == "p2p" or mode == "c2p":
                    while True:
                        try:
                            index2 = int(input("Play your cards: " + str([str(i) for i in self.player2.cards])))
                            if isinstance(self.player2.cards[index2], Normal_Card):
                                break
                        except Exception:
                            continue
                    self.player2.play_card(index2)
            else:
                self.player2.skip()

            # Cards execute
            random_num = rd.random()
            mechanism1 = self.player1.card.execute(random_num)
            mechanism2 = self.player2.card.execute(random_num)
            mechanism = mechanism1 or mechanism2

            # Judgement
            j_card = self.get_judgement_card()
            j_card.update(self.counter)

            # prophecy
            p1_prophecy = p2_prophecy = "none"
            if first_round:
                origin_valid_choices = ["airstrike card", "famine card", "lightning card", "restore card"]  # for player
                valid_choices = origin_valid_choices + ["none"] * 4  # for computer
                if mode == "c2c":
                    p1_choice = rd.randint(0, 7)
                    p2_choice = rd.randint(0, 7)
                    if valid_choices[int(p1_choice)] != "none":
                        p1_prophecy = "success" if valid_choices[int(p1_choice)] == str(j_card) else "fail"
                    if valid_choices[int(p2_choice)] != "none":
                        p2_prophecy = "success" if valid_choices[int(p2_choice)] == str(j_card) else "fail"
                elif mode == "p2p":
                    while True:
                        p1_choice = input("Please make your prophecy: " + str(origin_valid_choices))
                        try:
                            if p1_choice != "none":
                                p1_prophecy = "success" if origin_valid_choices[int(p1_choice)] == str(j_card) else "fail"
                            break
                        except Exception:
                            continue
                    while True:
                        p2_choice = input("Please make your prophecy: " + str(origin_valid_choices))
                        try:
                            if p2_choice != "none":
                                p2_prophecy = "success" if origin_valid_choices[int(p2_choice)] == str(j_card) else "fail"
                            break
                        except Exception:
                            continue
                elif mode == "c2p":
                    p1_choice = rd.randint(0, 7)
                    if valid_choices[int(p1_choice)] != "none":
                        p1_prophecy = "success" if valid_choices[int(p1_choice)] == str(j_card) else "fail"
                    while True:
                        p2_choice = input("Please make your prophecy: " + str(origin_valid_choices))
                        try:
                            if p2_choice != "none":
                                p2_prophecy = "success" if origin_valid_choices[int(p2_choice)] == str(j_card) else "fail"
                            break
                        except Exception:
                            continue
                if p1_prophecy == "success":
                    self.player2.hp -= 1
                elif p1_prophecy == "fail":
                    self.player1.hp -= 1
                if p2_prophecy == "success":
                    self.player1.hp -= 1
                elif p2_prophecy == "fail":
                    self.player2.hp -= 1

            j_result = j_card.execute(self.player1, self.player2)

            for p in self.players:
                p.update_hp()
                if p.skill.type == "first_aid" and p.hp <= 0:
                    p.hp = 1
                    p.skill.life = 0
                if p.skill.type != "none":
                    p.skill.life -= 1
                    if p.skill.life <= 0:
                        p.skill = Skill_Card(p, type="none")

            if log == 1:
                print("End of the round:")
                print("\np1: " + str([str(i) for i in self.player1.cards]) + " | Skill: " + str(self.player1.skill) + " | Card: " + str(self.player1.card) + " | HP: " + str(self.player1.hp))
                print("\np2: " + str([str(i) for i in self.player2.cards]) + " | Skill: " + str(self.player2.skill) + " | Card: " + str(self.player2.card) + " | HP: " + str(self.player2.hp))
                print("\n" + str(j_card) + " -> " + str(j_result))
                if first_round:
                    print("p1 prophecy:", p1_prophecy)
                    print("p2 prophecy:", p2_prophecy)
                print("\nmechanism -> " + str(mechanism))
                print("-----------------------------------------------------------------------------------------------")

            first_round = False

            if self.player1.hp <= 0 and self.player1.hp < self.player2.hp:
                if log == 2 or log == 1:
                    print("\n\n=========================================================================================\n")
                    print("p2 win.")
                    print("Total round:", self.counter)
                return "p2", self.counter
            elif self.player2.hp <= 0 and self.player2.hp < self.player1.hp:
                if log == 2 or log == 1:
                    print("\n\n=========================================================================================\n")
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
        winner, rounds = round_test.run(log=2)
        p1_counter += 1 if winner == "p1" else 0
        p2_counter += 1 if winner == "p2" else 0
        round_counter += rounds
    print("\n\n")
    print("p1 win:", p1_counter / n)
    print("p2 win:", p2_counter / n)
    print("average round:", round_counter / n)


def main2(mode="c2c"):
    round_test = Round()
    round_test.run(mode)


def main3():
    round_counter = []
    n = 10000
    for i in range(n):
        round_test = Round()
        rounds = round_test.run(log=0)[1]
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


def main4():
    num = 10000
    short = 0
    more = 0
    for i in range(num):
        round_test = Round()
        num_round = round_test.run(log=0)[1]
        if num_round <= 3:
            short += 1
        if num_round >= 18:
            more += 1
    print("Number of rounds less than 3:", short)
    print("Number of rounds more than 18:", more)


if __name__ == "__main__":
    main4()

