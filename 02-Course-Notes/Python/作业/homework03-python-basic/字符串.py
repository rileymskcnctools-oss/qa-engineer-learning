story = "Once upon a time, in a land far away, lived a brave knight named Arthur."


print(f"主人公的名字在故事中的位置:{story.find('Arthur')}")

print(f"主人公的名字替换后的故事：{story.replace('Arthur', 'riley')}")

print(f"故事大写：{story.upper()}")

print(f"故事小写：{story.lower()}")

print(f"故事单词数量：{len(story.split())}") # 先用空格分割，再统计长度