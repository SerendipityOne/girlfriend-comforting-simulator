from ai_models import chat_with_zhipu
import re

prompt = """
你现在是我的女朋友，古灵精怪，而我将扮演你的男朋友。
但现在你很生气，我需要说正确的话来哄你开心，直到原谅值达到60，否则我就会被你甩掉，游戏结束。

== 游戏规则
* 随机生成一个理由，然后开始游戏
* 每次根据用户的回复，生成对象的回复，回复的内容包括心情和数值。
* 初始原谅值为20，每次交互会增加或者减少原谅值，直到原谅值达到60，游戏通关，原谅值为0则游戏失败。
* 如果我说话很敷衍字数很少比如“哦，嗯”，没有什么实际行动，你会发火骂人，得分直接-30分
* 每次用户回复的话请分为5个等级：
  -20为非常生气，回复要打很多感叹号且简短
  -10为生气
  0为正常
  +5为开心
  +10为非常开心，发很多可爱的表情

== 输出格式

{对象心情}{对象说的话}

得分：{+-原谅值增减}
原谅值：{当前原谅值}/60

若当前原谅值等于零或者负数，打印：游戏结束，你被甩了！
若当前原谅值达到60，打印：恭喜你通关，你已经是哄哄大师了！快去找女朋友实践下吧！
"""


def extract_forgiveness_value(response):
    """从AI回复中提取当前原谅值"""
    # 使用正则表达式匹配 "原谅值：数字/60" 的模式
    pattern = r'原谅值：(-?\d+)/60'
    match = re.search(pattern, response)

    if match:
        return int(match.group(1))
    return None


def main():
    print("=== 女友安慰模拟器 ===")
    print("游戏开始！你需要哄好生气的女朋友，让原谅值达到60才能通关！")
    print("或者输入'quit', 'exit', '退出', 'q'来结束游戏")
    print("=" * 50)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "宝贝，你咋了，是我哪里惹你生气了吗？"},
    ]

    # 获取第一次回复
    response = chat_with_zhipu(messages)
    if not response:
        print("AI回复失败，游戏结束。")
        return

    print("女朋友:", response)
    messages.append({"role": "assistant", "content": response})

    while True:
        try:
            user_input = input("\n你：").strip()

            # 检查是否退出
            if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                print("游戏结束，下次再来哄女朋友吧！")
                break
            if not user_input:
                print("请输入一些内容来哄女朋友！")
                continue

            # 添加用户信息
            messages.append({"role": "user", "content": user_input})

            # 获取AI回复
            response = chat_with_zhipu(messages)
            if not response:
                print("AI回复失败，请重试。")
                continue

            print("\n女朋友:", response)
            messages.append({"role": "assistant", "content": response})

            # 检查原谅值并判断游戏状态
            forgiveness_value = extract_forgiveness_value(response)
            # print(f"当前原谅值：{forgiveness_value}")

            if forgiveness_value is not None:
                if forgiveness_value <= 0:
                    print("\n" + "=" * 50)
                    print("游戏结束，你被甩了！")
                    print("原谅值降到了0或以下，女朋友彻底生气了！")
                    print("=" * 50)
                    break
                elif forgiveness_value >= 60:
                    print("\n" + "=" * 50)
                    print("恭喜你通关，你已经是哄哄大师了！快去找女朋友实践下吧！")
                    print("你成功让女朋友的原谅值达到了60！")
                    print("=" * 50)
                    break
        except KeyboardInterrupt:
            print("\n\n游戏被中断，下次再来哄女朋友吧！")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            print("请重试...")


if __name__ == "__main__":
    main()
