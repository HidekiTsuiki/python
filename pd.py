''' 繰り返し囚人のジレンマ（戦略大会）で使うクラスと関数

    from pd import *
として使う。

戦略はクラスとして作る。1回の対戦ごとに，新しいインスタンスが作られる。
    choice(self)          次の手 'C'（協調）か 'D'（裏切り）を返す。
    learn(self, my, other) 今の回の自分の手 my と相手の手 other を教えてもらう。
                           （ノイズがある時は，ノイズで反転した後の実際の手）

利得（自分の得点）：
                相手 C   相手 D
    自分 C        3        0
    自分 D        5        1

1回の対戦は，毎回 PEND の確率で終わる（平均 1/PEND 回）。何回で終わるかは分からない。
NOISE の確率で，出した手が反転する（手が滑る）。
得点は，1回あたりの平均得点（0 から 5 の間）で表す。

禁止事項：相手のオブジェクトの中を覗くこと，乱数の種（random.seed）を操作すること，
他の参加者と示し合わせること，1回の choice, learn に長い時間をかけること。
'''
import random
import numpy as np

PAYOFF = {('C', 'C'): 3, ('C', 'D'): 0, ('D', 'C'): 5, ('D', 'D'): 1}
PEND = 0.01    # 各回で対戦が終わる確率
NOISE = 0.02   # 手が反転する確率


# ---------------- 主催者の戦略 ----------------

class AllC:
    '''いつも協調'''
    def choice(self):
        return 'C'

    def learn(self, my, other):
        return


class AllD:
    '''いつも裏切り'''
    def choice(self):
        return 'D'

    def learn(self, my, other):
        return


class RandomS:
    '''ランダムに協調か裏切り'''
    def choice(self):
        return random.choice('CD')

    def learn(self, my, other):
        return


class Alternate:
    '''協調と裏切りを交互に'''
    def __init__(self):
        self.my = 'C'

    def choice(self):
        return self.my

    def learn(self, my, other):
        self.my = 'D' if self.my == 'C' else 'C'


class TitForTat:
    '''しっぺ返し：最初は協調，あとは相手の前の手をまねる'''
    def __init__(self):
        self.my = 'C'

    def choice(self):
        return self.my

    def learn(self, my, other):
        self.my = other


class SuspiciousTFT:
    '''疑い深いしっぺ返し：最初は裏切り，あとは相手の前の手をまねる'''
    def __init__(self):
        self.my = 'D'

    def choice(self):
        return self.my

    def learn(self, my, other):
        self.my = other


class GenerousTFT:
    '''寛容なしっぺ返し：相手が裏切っても 1/3 の確率で許す'''
    def __init__(self):
        self.my = 'C'

    def choice(self):
        return self.my

    def learn(self, my, other):
        if other == 'D' and random.uniform(0, 1) < 1 / 3:
            self.my = 'C'
        else:
            self.my = other


class TitForTwoTats:
    '''相手が2回続けて裏切ったら裏切る'''
    def __init__(self):
        self.count = 0

    def choice(self):
        return 'D' if self.count >= 2 else 'C'

    def learn(self, my, other):
        self.count = self.count + 1 if other == 'D' else 0


class Grim:
    '''一度でも裏切られたら，それからずっと裏切る'''
    def __init__(self):
        self.angry = False

    def choice(self):
        return 'D' if self.angry else 'C'

    def learn(self, my, other):
        if other == 'D':
            self.angry = True


class Pavlov:
    '''勝てば同じ手，負ければ手を変える（win-stay, lose-shift）
       得点が 3 か 5 なら同じ手，0 か 1 なら手を変える'''
    def __init__(self):
        self.my = 'C'

    def choice(self):
        return self.my

    def learn(self, my, other):
        if PAYOFF[(my, other)] < 3:
            self.my = 'D' if my == 'C' else 'C'
        else:
            self.my = my


class Joss:
    '''しっぺ返しだが，10% の確率でこっそり裏切る'''
    def __init__(self):
        self.my = 'C'

    def choice(self):
        if random.uniform(0, 1) < 0.1:
            return 'D'
        return self.my

    def learn(self, my, other):
        self.my = other


HOUSE = [AllC, AllD, RandomS, Alternate, TitForTat, SuspiciousTFT,
         GenerousTFT, TitForTwoTats, Grim, Pavlov, Joss]


# ---------------- 対戦 ----------------

def flip(x):
    return 'D' if x == 'C' else 'C'


def Match(A, B, noise=NOISE, pend=PEND, seed=None):
    ''' 戦略クラス A と B を1回対戦させる。
    (A の1回あたりの平均得点, B の1回あたりの平均得点, 回数) を返す。
    seed を与えると，同じ seed なら同じ乱数で対戦する。'''
    if seed is not None:
        random.seed(seed)
    rng = random.Random(seed)   # 対戦の長さとノイズ用（戦略の乱数とは別）
    a, b = A(), B()
    sa, sb, n = 0, 0, 0
    while True:
        x, y = a.choice(), b.choice()
        if rng.uniform(0, 1) < noise:
            x = flip(x)
        if rng.uniform(0, 1) < noise:
            y = flip(y)
        a.learn(x, y)
        b.learn(y, x)
        sa += PAYOFF[(x, y)]
        sb += PAYOFF[(y, x)]
        n += 1
        if rng.uniform(0, 1) < pend:
            return sa / n, sb / n, n


def Evaluate(S, reps=100, noise=NOISE, pend=PEND, show=True):
    ''' 戦略クラス S を，主催者の戦略それぞれと reps 回ずつ対戦させる（採点用）。
    乱数の種は固定しているので，同じ戦略なら何度やっても同じ結果になる。
    相手ごとの平均得点の dict と，全体の平均得点を返す。'''
    res = {}
    for j, B in enumerate(HOUSE):
        res[B.__name__] = float(np.mean([Match(S, B, noise, pend, seed=1000 * j + r)[0]
                                   for r in range(reps)]))
    total = float(np.mean(list(res.values())))
    if show:
        for k, v in res.items():
            print(f'{k:>14s} : {v:.3f}')
        print(f'{"平均":>13s} : {total:.3f}')
        print(f'{"対戦点":>12s} : {Points(total)} / 10')
    return res, total


_BASE = None


def Points(total):
    ''' Evaluate の平均得点を，対戦点（10 点満点）に換算する。
    しっぺ返し（TitForTat）と同じ平均得点で 6 点，それより 0.05 高いごとに 1 点増える
    （低ければ減る）。0 点から 10 点の範囲におさめ，小数第1位まで。'''
    global _BASE
    if _BASE is None:
        _BASE = Evaluate(TitForTat, show=False)[1]
    p = 6 + (total - _BASE) / 0.05
    return round(float(min(max(p, 0), 10)), 1)


def Tournament(strategies, reps=20, noise=NOISE, pend=PEND):
    ''' 戦略クラスのリストで総当たり戦を行う（自分自身のコピーとも対戦する）。
    M[i][j] = i が j と対戦した時の i の平均得点 となる行列 M と，
    各戦略の平均得点を返す。'''
    k = len(strategies)
    M = np.zeros((k, k))
    for i in range(k):
        for j in range(i, k):
            r = np.array([Match(strategies[i], strategies[j], noise, pend,
                                seed=100000 * i + 1000 * j + t)[:2] for t in range(reps)])
            M[i][j] = r[:, 0].mean()
            M[j][i] = r[:, 1].mean()
    return M, M.mean(axis=1)


def ShowTournament(strategies, M, total):
    ''' Tournament の結果を得点の高い順に表示する '''
    for i in np.argsort(-total):
        print(f'{strategies[i].__name__:>14s} : {total[i]:.3f}')
