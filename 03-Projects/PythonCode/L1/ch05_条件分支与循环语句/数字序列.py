from random import randint

play_v = 0
bot_v = 0

for i in range(3):

    bot = randint(1, 6)

    play = int(input("请输入一个1-6之间的数字："))

    while play > 6 or play < 1:
        print("请输入正确的数字")
        play = int(input("请输入一个1-6之间的数字："))

    if play == bot:
        pass

    elif play > bot:
        play_v += 1
        print(f"玩家{play}点，电脑{bot}点，玩家胜")

    else:
        bot_v += 1
        print(f"玩家{play}点，电脑{bot}点，电脑胜")


if play_v > bot_v:
    print(f"玩家赢{play_v}局，电脑赢{bot_v}局，玩家胜利")

elif play_v < bot_v:
    print(f"玩家赢{play_v}局，电脑赢{bot_v}局，电脑胜利")

else:
    print(f"玩家赢{play_v}局，电脑赢{bot_v}局，平局")
