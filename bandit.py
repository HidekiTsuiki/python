''' 多腕バンディット問題（第10回，第11回）で使うクラスと関数

    from bandit import *
として使う。
'''
import random
import numpy as np


class Bandit:
    '''スロットマシン  確率 p で 1, 1-p で 0 を返す （ベルヌーイ分布）
         インスタンス変数：p   ランダムに [0, 1] の値が設定されている。
         メソッド：
            slot() スロットを引く。確率 p で 1, 1-p で 0 が返ってくる。
    '''
    def __init__(self):
        self.p = random.uniform(0, 1)

    def slot(self):
        if random.uniform(0, 1) < self.p:
            return 1
        else:
            return 0

    def update(self):
        '''1/2 の確率で，0.05 上げるか下げるか。
        0 より小さく，1 より大きくはならない。'''
        if random.uniform(0, 1) < 0.5:
            self.p = max(self.p - 0.05, 0)
        else:
            self.p = min(self.p + 0.05, 1)


class MultiArmedBandit:
    '''スロットマシンを NUM 個まとめたもの
         クラス変数：NUM  スロットマシンの個数 (定数)
         インスタンス変数：bandits スロットマシンのリスト
         メソッド：
            slot(i) i 番目のスロットを引く。
            getmax() スロットマシンの確率の最大値を返す。
    '''
    NUM = 10   # スロットマシンの個数

    def __init__(self):
        self.bandits = [Bandit() for i in range(MultiArmedBandit.NUM)]

    def slot(self, i):
        '''i 番目のスロットマシンを引く'''
        if i < 0 or i >= MultiArmedBandit.NUM:
            return 0
        return self.bandits[i].slot()

    def update(self):
        '''全ての確率を更新する（change=True の時に使う）'''
        for b in self.bandits:
            b.update()

    def getmax(self):
        return max([x.p for x in self.bandits])

    def getmaxind(self):
        maxi = 0
        for i in range(len(self.bandits)):
            if self.bandits[maxi].p < self.bandits[i].p:
                maxi = i
        return maxi


class RandomStrategy:
    ''' ランダムにスロットマシンを引く戦略 '''
    def __init__(self, n):
        self.n = n

    def learn(self, k, result):
        return

    def choice(self):
        return random.randrange(self.n)

    def reset(self):
        return


class TsuikiStrategy:
    ''' 前のが当たったらそれを引く戦略
    インスタンス変数:
        n : スロットマシンの台数
        my : 次に引く手
    '''
    def __init__(self, n):
        self.n = n
        self.my = 0

    def learn(self, k, result):
        if result == 0:
            self.my = (self.my + 1) % self.n

    def choice(self):
        return self.my

    def reset(self):
        self.my = 0


class MaxStrategy:
    ''' してはいけないことをして，最高確率のスロットマシンを引く戦略（比較の基準） '''
    def __init__(self, m):
        self.mab = m

    def learn(self, k, result):
        return

    def choice(self):
        return self.mab.getmaxind()

    def reset(self):
        return


def OnePlay(numplay, strategies, mab, change=False):
    ''' strategies : 戦略のリスト
    結果は，それぞれの戦略での当たり確率を，ndarray として返す。'''
    myaccounts = np.zeros(len(strategies), dtype=int)
    for x in strategies:
        x.reset()

    for i in range(numplay):
        for s in range(len(strategies)):
            k = strategies[s].choice()
            result = mab.slot(k)
            myaccounts[s] += result
            strategies[s].learn(k, result)
        if change:
            mab.update()  # 確率が変化していく場合
    return myaccounts / numplay


def MultiMABTester(n, strategyClasses, change=False, numplay=300):
    ''' n 回のゲーム（1ゲームは numplay 回引く）を行い，
    各戦略の当たり確率を，(戦略の数+1) x n の ndarray として返す。最後の行は MaxStrategy の結果。'''
    ret = np.zeros((len(strategyClasses) + 1, 0))
    for i in range(n):
        mab = MultiArmedBandit()
        strategies = [a(MultiArmedBandit.NUM) for a in strategyClasses]
        strategies.append(MaxStrategy(mab))
        ret = np.append(ret, OnePlay(numplay, strategies, mab, change).reshape(len(strategies), 1), axis=1)
    return ret
