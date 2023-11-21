
''' 階乗関数のモジュール'''
a = 1
def fact(n):
    '''n の階乗を計算する'''
    if(n == 1):
        return a
    print("name is", __name__)
    return n*fact(n-1)

fact100 = fact(100)
print(fact(10))
if (__name__ == "__main__"):
    print(fact(int(input("数を入力してください:"))))
