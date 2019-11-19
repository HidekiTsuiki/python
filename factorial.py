''' 階乗関数のモジュール'''
a = 1
def fact(n):
    '''n の階乗を計算する'''
    ret = 1
    for i in range(1,n+1):
        ret *= i
    return ret

fact100 = fact(100)
print(fact(10))
if (__name__ == "__main__"):
    print(fact(int(input("数を入力してください:"))))
