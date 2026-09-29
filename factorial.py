''' 階乗関数のモジュール'''
a = 1
def fact(n):
    '''n の階乗を計算する'''
    r = a
    for i in range(2, n + 1):
        r = r * i
#    print("name is", __name__)
    return r

fact100 = fact(100)
print(fact(10))
# if __name__ == "__main__":
#     print(fact(int(input("数を入力してください:"))))
