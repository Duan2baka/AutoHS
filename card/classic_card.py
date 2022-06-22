from card.basic_card import *


# 闪电箭
class LightingBolt(SpellPointOppo):
    spell_type = SPELL_POINT_OPPO
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_power = state.my_total_spell_power
        damage = 3 + spell_power
        best_delta_h = state.oppo_hero.delta_h_after_damage(damage)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            delta_h = oppo_minion.delta_h_after_damage(damage)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 呱
class Hex(SpellPointOppo):
    bias = -6
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue

            delta_h = oppo_minion.heuristic_val - 1

            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


# 闪电风暴
class LightningStorm(SpellNoPoint):
    bias = -10

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        spell_power = state.my_total_spell_power

        for oppo_minion in state.oppo_minions:
            h_sum += (oppo_minion.delta_h_after_damage(2 + spell_power) +
                      oppo_minion.delta_h_after_damage(3 + spell_power)) / 2

        return h_sum + cls.bias,


# TC130
class MindControlTech(MinionNoPoint):
    value = 0.2
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.oppo_minion_num < 4:
            return cls.value, state.my_minion_num
        else:
            h_sum = sum([minion.heuristic_val for minion in state.oppo_minions])
            h_sum /= state.oppo_minion_num
            return cls.value + h_sum * 2,


# 野性狼魂
class FeralSpirit(SpellNoPoint):
    value = 2.4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_minion_num >= 7:
            return -1, 0
        else:
            return cls.value, 0


# 碧蓝幼龙
class AzureDrake(MinionNoPoint):
    value = 3
    keep_in_hand_bool = False


# 奥妮克希亚
class Onyxia(MinionNoPoint):
    value = 10
    keep_in_hand_bool = False


# 火元素
class FireElemental(MinionPointOppo):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        best_h = 3 + state.oppo_hero.delta_h_after_damage(3)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = 3 + oppo_minion.delta_h_after_damage(3)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index


# 精灵弓箭手
class ElvenArcher(MinionPointOppo):
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        # 不能让她下去点脸, 除非对面快死了
        best_h = -0.8 + state.oppo_hero.delta_h_after_damage(1)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = -0.5 + oppo_minion.delta_h_after_damage(1)
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index


# 大地之环先知
class EarthenRingFarseer(MinionPointMine):
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        best_h = 0.2 + state.my_hero.delta_h_after_heal(3)
        if state.my_hero.health <= 5:
            best_h += 4
        best_my_index = -1

        for my_index, my_minion in enumerate(state.my_minions):
            delta_h = -0.5 + my_minion.delta_h_after_heal(3)
            if delta_h > best_h:
                best_h = delta_h
                best_my_index = my_index

        return best_h, state.my_minion_num, best_my_index


# 憎恶
class Abomination(MinionNoPoint):
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        for oppo_minion in state.oppo_minions:
            h_sum += oppo_minion.delta_h_after_damage(2)
        for my_minion in state.my_minions:
            h_sum -= my_minion.delta_h_after_damage(2)
        h_sum += state.oppo_hero.delta_h_after_damage(2)
        h_sum -= state.my_hero.delta_h_after_damage(2)

        return h_sum,


# 狂奔科多兽
class StampedingKodo(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_sum = 2
        temp_sum = 0
        temp_count = 0

        for oppo_minion in state.oppo_minions:
            if oppo_minion.attack <= 2:
                temp_sum += oppo_minion.heuristic_val
                temp_count += 1
        if temp_count > 0:
            h_sum += temp_sum / temp_count

        return h_sum,


# 血骑士
class BloodKnight(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_sum = 1

        for oppo_minion in state.oppo_minions:
            if oppo_minion.divine_shield:
                h_sum += oppo_minion.attack + 6
        for my_minion in state.my_minions:
            if my_minion.divine_shield:
                h_sum += -my_minion.attack + 6

        return h_sum,


# 末日
class DoomSayer(MinionNoPoint):
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        # 一费别跳末日
        if state.my_total_mana == 1:
            return 0,

        # 二三费压末日就完事了
        if state.my_total_mana <= 3:
            return 1000,

        # 优势不能上末日
        if state.my_heuristic_value >= state.oppo_heuristic_value:
            return 0,

        oppo_attack_sum = 0
        for oppo_minion in state.oppo_minions:
            oppo_attack_sum += oppo_minion.attack

        if oppo_attack_sum >= 7:
            # 当个嘲讽也好
            return 1,
        else:
            return state.oppo_heuristic_value - state.my_heuristic_value,


class StormforgedAxe(WeaponCard):
    keep_in_hand_bool = True
    value = 1.5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        # 不要已经有刀了再顶刀
        if state.my_weapon is not None:
            return 0,
        if state.my_total_mana == 2:
            for oppo_minion in state.touchable_oppo_minions:
                # 如果能提起刀解了, 那太好了
                if oppo_minion.health <= 2 and \
                        not oppo_minion.divine_shield:
                    return 2000,

        return cls.value,

#鹰角弓
class EaglehornBow(WeaponCard):
    keep_in_hand_bool = False
    value = 2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        # 不要已经有刀了再顶刀
        if state.my_weapon is not None:
            return 0,
        if state.my_total_mana == 3:
            for oppo_minion in state.touchable_oppo_minions:
                # 如果能提起刀解了, 那太好了
                if oppo_minion.health <= 3 and \
                        not oppo_minion.divine_shield:
                    return 5,

        return cls.value,


#关门放狗
class UnleashTheHounds(SpellNoPoint):
    bias = -10
    keep_in_hand_bool = False
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        spell_power = state.my_total_spell_power
        total_num = min((7-state.my_minion_num),state.oppo_minion_num)
        return  total_num * 0.9,

#动物伙伴
class AnimalCompanion(SpellNoPoint):
    value = 3
    keep_in_hand_bool = True
    
#长鬃草原狮
class Highmane(MinionNoPoint):
    value = 7
    keep_in_hand_bool = False

#铁喙猫头鹰
class IronbeakOwl(MinionPointOppo):
    keep_in_hand_bool = False
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        best_h = -2
        best_oppo_index = -1
        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = oppo_minion.taunt + oppo_minion.divine_shield + oppo_minion.windfury + 1
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index

#变形术
class Polymorph(SpellPointOppo):
    bias = -6
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue

            delta_h = oppo_minion.heuristic_val - 1

            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,

#水元素
class WaterElemental(MinionNoPoint):
    value = 3.5
    keep_in_hand_bool = True

#火球术
class FireBall(SpellPointOppo):
    spell_type = SPELL_POINT_OPPO
    keep_in_hand_bool = False
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_power = state.my_total_spell_power
        damage = 6 + spell_power
        best_delta_h = state.oppo_hero.delta_h_after_damage(damage)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            delta_h = oppo_minion.delta_h_after_damage(damage)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,

#火车王当火球用(没判断嘲讽)
class LeeroyJenkins(MinionNoPoint):
    keep_in_hand_bool = False
    bias = -4

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        damage = 6 
        best_delta_h = state.oppo_hero.delta_h_after_damage(damage)

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            delta_h = oppo_minion.delta_h_after_damage(damage)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
        return best_delta_h + cls.bias,

# 寒冰箭
class FrostBolt(SpellPointOppo):
    spell_type = SPELL_POINT_OPPO
    bias = -2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_power = state.my_total_spell_power
        damage = 3 + spell_power
        best_delta_h = state.oppo_hero.delta_h_after_damage(damage)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            delta_h = oppo_minion.delta_h_after_damage(damage)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,

#奥术智慧
class ArcaneIntellect(SpellNoPoint):
    keep_in_hand_bool = False
    value = 2

#奥术飞弹
class ArcaneMissiles(SpellNoPoint):
    keep_in_hand_bool = False
    bias = 0
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        h_sum = 0
        spell_power = state.my_total_spell_power
        damage = spell_power + 3
        num = len(state.oppo_minions) + 1
        for oppo_minion in state.oppo_minions:
            P = 1 / num
            for dmg in range(0,damage+1):
                h_sum += P * oppo_minion.delta_h_after_damage(dmg)
                P= P / num
        P = 1 / num
        for dmg in range(0,damage+1):
            h_sum += P * state.oppo_hero.delta_h_after_damage(dmg)
            P = 1 / num
        #print(h_sum)
        return h_sum + cls.bias,

class Innervate(SpellNoPoint):
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

class Swipe(SpellPointOppo):
    spell_type = SPELL_POINT_OPPO
    keep_in_hand_bool = False
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_power = state.my_total_spell_power
        best_delta_h = state.oppo_hero.delta_h_after_damage(spell_power + 4)
        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            best_delta_h += oppo_minion.delta_h_after_damage(spell_power + 1)
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            delta_h = state.oppo_hero.delta_h_after_damage(spell_power + 1)
            delta_h = oppo_minion.delta_h_after_damage(spell_power + 4)
            for other_oppo_index, other_oppo_minion in enumerate(state.oppo_minions):
                if oppo_index != other_oppo_index:
                    delta_h += oppo_minion.delta_h_after_damage(spell_power + 1)
            if best_delta_h < delta_h:
                best_delta_h = delta_h
                best_oppo_index = oppo_index

        return best_delta_h + cls.bias, best_oppo_index,


#炽炎战斧
class FieryWarAxe(WeaponCard):
    keep_in_hand_bool = True
    value = 2.5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        # 不要已经有刀了再顶刀
        if state.my_weapon is not None:
            return 0,
        if state.my_total_mana == 2:
            for oppo_minion in state.touchable_oppo_minions:
                # 如果能提起刀解了, 那太好了
                if oppo_minion.health <= 3 and \
                        not oppo_minion.divine_shield:
                    return 5,

        return cls.value,

#格罗玛什·地狱咆哮
class GrommashHellscream(MinionNoPoint):
    value = 10
    keep_in_hand_bool = False

class TruesilverChampion(WeaponCard):
    keep_in_hand_bool = False
    value = 3.5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        # 不要已经有刀了再顶刀
        if state.my_weapon is not None:
            return 0,
        if state.my_total_mana == 4:
            for oppo_minion in state.touchable_oppo_minions:
                # 如果能提起刀解了, 那太好了
                if oppo_minion.health <= 4 and \
                        not oppo_minion.divine_shield:
                    return 5,

        return cls.value,


class TirionFordring(MinionNoPoint):
    value = 10
    keep_in_hand_bool = False

class Consecration(SpellNoPoint):
    bias = -10
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_power = state.my_total_spell_power
        h_sum = state.oppo_hero.delta_h_after_damage(2 + spell_power)

        for oppo_minion in state.oppo_minions:
            h_sum += oppo_minion.delta_h_after_damage(2 + spell_power)

        return h_sum + cls.bias,
