import random
import time
from abc import ABC, abstractmethod
import click
from constants.constants import *


class Card(ABC):
    value = 0

    # 返回两个东西,第一项是使用这张卡的\delta h,
    # 之后是是用这张卡的最佳参数,参数数目不定
    # 参数是什么呢,比如一张火球术,参数就是指示你
    # 是要打脸还是打怪
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.value

    @classmethod
    @abstractmethod
    def use_with_arg(cls, state, card_index, *args):
        pass

    @classmethod
    @abstractmethod
    def get_card_type(cls):
        pass


class SpellCard(Card):
    wait_time = 1.5

    @classmethod
    def get_card_type(cls):
        return CARD_SPELL


class SpellNoPoint(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        click.choose_and_use_spell(card_index, state.my_hand_card_num)
        click.cancel_click()
        time.sleep(cls.wait_time)


class SpellPointOppo(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        if len(args) == 0:
            hand_card = state.my_hand_cards[card_index]
            return

        oppo_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_oppo_hero()
        click.cancel_click()
        time.sleep(cls.wait_time)


class SpellPointMine(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        if len(args) == 0:
            hand_card = state.my_hand_cards[card_index]
            return

        mine_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        click.choose_my_minion(mine_index, state.oppo_minion_num)
        click.cancel_click()
        time.sleep(cls.wait_time)


class MinionCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_MINION


class MinionNoPoint(MinionCard):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        # 格子满了
        if state.my_minion_num == 7:
            return -1, 0
        elif cls.value != 0:
            return cls.value, state.my_minion_num
        else:
            hand_card = state.my_hand_cards[hand_card_index]
            # 在什么都不知道的时候, 认为费用越高的卡应该越超模
            return hand_card.current_cost / 2 + 1, state.my_minion_num  # 默认放到最右边

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)


class MinionPointOppo(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        oppo_index = args[1]

        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_oppo_hero()
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)


class WeaponCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_WEAPON

    # TODO: 还什么都没实现...


class HeroPowerCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_HERO_POWER


# 幸运币
class Coin(SpellNoPoint):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0

        for another_index, hand_card in enumerate(state.my_hand_cards):
            delta_h = 0

            if hand_card.current_cost != state.my_last_mana + 1:
                continue
            if hand_card.is_coin:
                continue

            detail_card = hand_card.detail_card
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    delta_h = MinionNoPoint.best_h_and_arg(state, another_index)[0]
            else:
                delta_h = detail_card.best_h_and_arg(state, another_index)[0]

            delta_h -= 1  # 如果跳费之后能使用的卡显著强于不跳费的卡, 就跳币
            best_delta_h = max(best_delta_h, delta_h)

        return best_delta_h,
