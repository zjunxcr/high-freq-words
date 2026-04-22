#!/usr/bin/env python3
"""
老友记场景升级：单句 -> 多轮对话 + 词库补充至1000
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "frequency_1000.json"

# ============== 110个基础词的多轮对话（替换原有单句）============
DIALOGUES_V1 = {
    "a": (
        "Monica: Anyone want **a** coffee?\nJoey: I'll take **a** large one!\nChandler: Make that two. I need **a** break.",
        "莫妮卡：嘿，有人要来杯咖啡吗？\n乔伊：我要一大杯！\n钱德勒：算我一份。我需要休息一下。"
    ),
    "about": (
        "Ross: Let's talk **about** us.\nRachel: **About** us? What about us?\nRoss: I need to tell you **about** my feelings.\nRachel: Can we talk **about** this later?",
        "罗斯：我们来谈谈我们之间的事。\n瑞秋：关于我们？什么？\n罗斯：我想告诉你我的感受。\n瑞秋：这事能以后再谈吗？"
    ),
    "all": (
        "Phoebe: I invited **all** my friends!\nRoss: All of them? That's fifty people!\nPhoebe: Yeah! The more, the merrier!",
        "菲比：我邀请了我所有的朋友！\n罗斯：所有人？那大概有五十个人！\n菲比：对啊！人越多越热闹嘛！"
    ),
    "also": (
        "Chandler: Monica is cooking dinner tonight.\nJoey: Nice! What's she making?\nChandler: Pasta. She's **also** making garlic bread.\nJoey: I love that woman!",
        "钱德勒：莫妮卡今晚做饭。\n乔伊：太好了！她做什么？\n钱德勒：意面。她还做了蒜香面包。\n乔伊：我爱死她了！"
    ),
    "am": (
        "Joey: What time is it?\nMonica: It's eight. Why?\nJoey: I **am** late for my audition!\nRachel: Good luck, Joey!",
        "乔伊：几点了？\n莫妮卡：八点了。怎么了？\n乔伊：我试镜要迟到了！\n瑞秋：祝你好运，乔伊！"
    ),
    "an": (
        "Ross: I have **an** idea!\nRachel: Every time you say that...\nRoss: This time it's **an** excellent plan!\nRachel: We'll see about that.",
        "罗斯：我有个主意！\n瑞秋：每次你这么说……\n罗斯：这次是个极好的计划！\n瑞秋：那就走着瞧吧。"
    ),
    "and": (
        "Monica: Did you buy the milk **and** eggs?\nChandler: I got the milk...\nMonica: **And** the eggs?\nChandler: ...I forgot the eggs.",
        "莫妮卡：你买了牛奶和鸡蛋吗？\n钱德勒：牛奶买了……\n莫妮卡：那鸡蛋呢？\n钱德勒：……我忘了买鸡蛋。"
    ),
    "are": (
        "Phoebe: Where **are** we going tonight?\nRachel: We **are** going to that new restaurant.\nJoey: **are** you sure it's open?\nMonica: They **are** open until eleven.",
        "菲比：我们今晚去哪儿啊？\n瑞秋：我们去那家新餐厅。\n乔伊：确定开着门吗？\n莫妮卡：营业到十一点。"
    ),
    "as": (
        "Rachel: You're acting **as** if nothing happened!\nRoss: Well, what do you want me to say?\nRachel: Don't act **as** cool **as** usual!\nRoss: It's not **as** bad **as** you think.",
        "瑞秋：你表现得好像什么都没发生一样！\n罗斯：那你希望我说什么？\n瑞秋：别跟平时那么淡定！\n罗斯：没你想得那么严重。"
    ),
    "at": (
        "Chandler: Look **at** this! My boss wants me to work Saturday!\nMonica: Again? You were **at** the office all week!\nChandler: He said be **at** work at nine. What can I do?",
        "钱德勒：看看这个！老板要我周六加班！\n莫妮卡：又来？你这周都在公司待着了！\n钱德勒：他说九点到。我能怎么办？"
    ),
    "away": (
        "Monica: Joey, put that cookie down!\nJoey: What? It's just sitting there!\nMonica: Put it **away**! That's for dessert!",
        "莫妮卡：乔伊，把饼干放下！\n乔伊：什么？它就放在那儿嘛！\n莫妮卡：收起来！那是甜点！"
    ),
    "back": (
        "Rachel: Welcome **back**, Ross! How was London?\nRoss: It was... an experience.\nMonica: Glad to have you **back**!\nRoss: There's no place like home.",
        "瑞秋：欢迎回来，罗斯！伦敦怎么样？\n罗斯：挺难忘的。\n莫妮卡：很高兴你回来了！\n罗斯：还是家里好。"
    ),
    "be": (
        "Monica: Please **be** quiet! The baby is sleeping!\nChandler: Sorry! I didn't know.\nMonica: Just **be** careful when you walk by, okay?",
        "莫妮卡：请安静！宝宝在睡觉！\n钱德勒：抱歉！我不知道。\n莫妮卡：经过时小心一点好吗？"
    ),
    "because": (
        "Ross: Why did you break up with him?\nRachel: **Because** he was cheating on me!\nPhoebe: Because of that?\nRachel: Yes! That's a good reason, don't you think?",
        "罗斯：你为什么跟他分手？\n瑞秋：因为他劈腿！\n菲比：就因为那个？\n瑞秋：是的！这理由够充分了吧！"
    ),
    "been": (
        "Joey: Have you ever **been** to Italy?\nMonica: Yes, I've **been** there twice.\nJoey: Really? I've never **been** outside New York!\nChandler: That's sad, Joey.",
        "乔伊：你去过意大利吗？\n莫妮卡：去过两次。\n乔伊：真的？我从没出过纽约！\n钱德勒：这太可悲了，乔伊。"
    ),
    "but": (
        "Rachel: I really like this dress!\nMonica: **But** it's too expensive.\nRachel: **But** I look great in it!\nMonica: **But** you don't have money! Put it **back**!",
        "瑞秋：我真的喜欢这条裙子！\n莫妮卡：但是太贵了。\n瑞秋：但是我穿上去很好看啊！\n莫妮卡：但是你没钱啊！放回去吧！"
    ),
    "by": (
        "Phoebe: Who wrote this song?\nMike: Written **by** Paul McCartney.\nPhoebe: The Beatles guy? I love him!\nMike: And this painting is done **by** Monet.",
        "菲比：谁写的这首歌？\n迈克：保罗·麦卡特尼写的。\n菲比：披头士那个？我喜欢他！\n迈克：这幅画是莫奈画的。"
    ),
    "can": (
        "Monica: **Can** you help me with dinner?\nChandler: Sure, what do you need?\nMonica: **Can** you chop these vegetables?\nChandler: I **can** do that. I'm good at chopping things.",
        "莫妮卡：能帮我做晚饭吗？\n钱德勒：当然，需要什么？\n莫妮卡：能帮我把这些蔬菜切了吗？\n钱德勒：可以。我很擅长切东西。"
    ),
    "come": (
        "Ross: **Come** in! Door's open!\nRachel: Thanks! Sorry I'm late.\nRoss: No problem. **Come** sit down. Want to **come** to the movie later?\nRachel: I'd love to!",
        "罗斯：进来！门没锁！\n瑞秋：谢谢！我来晚了。\n罗斯：没事。过来坐会儿。等下想去看电影吗？\n瑞秋：很想！"
    ),
    "could": (
        "Rachel: **Could** you pass me the salt?\nMonica: Here.\nRachel: Thanks. **Could** I borrow your blue dress tomorrow?\nMonica: Could you ask before using my closet?",
        "瑞秋：能把盐递给我吗？\n莫妮卡：给你。\n瑞秋：谢谢。明天我能借你的蓝裙子穿吗？\n莫妮卡：你是不是该先问一声再打我衣柜的主意？"
    ),
    "day": (
        "Phoebe: What a beautiful **day**!\nJoey: Perfect for the beach!\nChandler: It's raining, Phoebe. Look outside.\nPhoebe: Every **day** is beautiful if you think positive!",
        "菲比：多美好的一天啊！\n乔伊：去海滩的好天气！\n钱德勒：外面下雨呢，菲比。\n菲比：心态积极的话每天都很美好！"
    ),
    "did": (
        "Monica: What **did** you do today?\nJoey: Nothing much. Why?\nMonica: **Did** you call that girl from the coffee shop?\nJoey: No... should I have?",
        "莫妮卡：你今天干什么了？\n乔伊：没干什么。怎么了？\n莫妮卡：你给咖啡店那个女孩打电话了吗？\n乔伊：没有……我应该打吗？"
    ),
    "do": (
        "Chandler: What **do** you want for your birthday?\nMonica: Surprise me!\nChandler: But what **do** you actually want?\nMonica: A surprise IS what I **do** want!",
        "钱德勒：你生日想要什么？\n莫妮卡：给我个惊喜！\n钱德勒：但你到底想要什么呀？\n莫妮卡：惊喜就是我要的！"
    ),
    "don't": (
        "Joey: **Don't** tell anyone, okay?\nRachel: What happened?\nJoey: Promise you won't say a word!\nRachel: Okay! I won't tell anyone!",
        "乔伊：别告诉任何人好吗？\n瑞秋：什么事？\n乔伊：保证不说出去！\n瑞秋：好的！我不会告诉任何人的！"
    ),
    "each": (
        "Monica: We'll split the bill. **Each** person pays their share.\nJoey: How much **each**?\nMonica: Twenty dollars **each**.\nJoey: Can I pay later?",
        "莫妮卡：AA制。每人付自己的那份。\n乔伊：每人多少？\n莫妮卡：每人二十美元。\n乔伊：能晚点付吗？"
    ),
    "find": (
        "Rachel: **Find** my keys! I can't find them anywhere!\nMonica: Check your bag.\nRachel: I can't **find** them!\nJoey: Wait — are these them?\nRachel: Joey! Where did you **find** those?!",
        "瑞秋：帮我找钥匙！哪儿都找不到！\n莫妮卡：看看包里。\n瑞秋：找不到啊！\n乔伊：等等——是这串吗？\n瑞秋：乔伊！你在哪儿找到的？！"
    ),
    "first": (
        "Chandler: **First**, let me explain.\nMonica: Better be good.\nChandler: **First**, it was an accident. **Second**, I didn't mean to...\nMonica: Stop with first and second! Tell me what happened!",
        "钱德勒：首先让我解释一下。\n莫妮卡：最好说清楚。\n钱德勒：首先是意外。其次我不是故意的……\n莫妮卡：别什么第一第二的了！直接告诉我发生了什么！"
    ),
    "for": (
        "Ross: This gift is **for** you.\nRachel: Really? What's it **for**?\nRoss: Just **for** being you.\nRachel: Aww, Ross... You shouldn't have!\nRoss: I wanted to. It's **for** you.",
        "罗斯：这是给你的礼物。\n瑞秋：真的？干嘛用的？\n罗斯：就因为你就是你。\n瑞秋：哎呀，罗斯……不用这样的！\n罗斯：我想送。这是给你的。"
    ),
    "from": (
        "Phoebe: Where are you **from** originally?\nMike: I'm **from** London, but I live here now.\nPhoebe: Cool! I'm **from**... well, it's complicated.\nMike: That's okay. I like complicated.",
        "菲比：你原籍哪里？\n迈克：来自伦敦，现在住这儿。\n菲比：酷！我是来自……嗯，说来话长。\n迈克：没关系。我喜欢复杂的。"
    ),
    "get": (
        "Monica: When will you **get** home tonight?\nChandler: Around seven. Why?\nMonica: I need you to **get** groceries on your way back.\nChandler: Sure. What do we need to **get**?",
        "莫妮卡：你今晚几点到家？\n钱德勒：大概七点。怎么了？\n莫妮卡：回来的路上买点菜。\n钱德勒：好的。需要买什么？"
    ),
    "give": (
        "Rachel: Can you **give** me a ride to work tomorrow?\nMonica: Sure. What time?\nRachel: Can you **give** me a call when you leave?\nMonica: I'll **give** you a call at eight.",
        "瑞秋：明天能载我一程去上班吗？\n莫妮卡：当然。几点？\n瑞秋：出发的时候给我打个电话？\n莫妮卡：八点我会打给你的。"
    ),
    "go": (
        "Joey: Let's **go** get some pizza!\nChandler: Again? We had pizza yesterday.\nJoey: Come on! Let's **go**! I'm starving!\nPhoebe: I'll **go** with you! I could eat a whole pizza right now!",
        "乔伊：咱们去买披萨吧！\n钱德勒：又是披萨？昨天才吃过。\n乔伊：走吧走吧！我饿死了！\n菲比：我跟你们去！我现在能吃下一整张披萨！"
    ),
    "going": (
        "Rachel: What's **going** on here? So quiet!\nMonica: We're planning a surprise party for you!\nRachel: For me? Really?\nChander: Yeah. Pretend nothing's **going** on.\nRachel: Got it! Wow, thanks guys!",
        "瑞秋：这里怎么回事？怎么这么安静？\n莫妮卡：我们在策划惊喜派对给你！\n瑞秋：给我？真的？\n钱德勒：对。假装什么都没发生。\n瑞秋：收到！哇，谢谢你们！"
    ),
    "good": (
        "Ross: How's the new job?\nRachel: Pretty **good** actually!\nRoss: That's **good** to hear.\nRachel: My coworkers are nice. It's a **good** place.",
        "罗斯：新工作怎么样？\n瑞秋：实际上挺好的！\n罗斯：听起来不错。\n瑞秋：同事都很好。是个好地方。"
    ),
    "got": (
        "Joey: **Got** any plans this weekend?\nChandler: Not really. Why?\nJoey: I **got** tickets to the game! Wanna go?\nChandler: You **got** tickets? How?! Those are impossible to **get**!",
        "乔伊：周末有什么安排？\n钱德勒：没什么特别的。怎么了？\n乔伊：我搞到比赛门票了！想去吗？\n钱德勒：搞到票了？怎么可能？！根本抢不到！"
    ),
    "great": (
        "Phoebe: That's a **great** idea, Mike!\nMike: Really? You think so?\nPhoebe: Yeah! Everything about you is **great**!\nChandler (to himself): They're so cute. It's **great**.",
        "菲比：这主意太棒了，迈克！\n迈克：真的？你是这么想的？\n菲比：是啊！你身上的一切都很棒！\n钱德勒（自言自语）：他们太可爱了。真好。"
    ),
    "had": (
        "Monica: I **had** such a long day today.\nChandler: What happened?\nMonica: Three meetings, and I **had** to cook dinner for twelve people!\nChandler: You **had** a busy day. Let me give you a massage.",
        "莫妮卡：我今天过得太累了。\n钱德勒：怎么了？\n莫妮卡：开了三个会，还要给十二个人做晚饭！\n钱德勒：确实辛苦了。让我给你按摩一下吧。"
    ),
    "has": (
        "Ross: She **has** the most beautiful smile.\nJoey: Who **has** a beautiful smile?\nRoss: Never mind. But she **has** amazing eyes too.\nJoey: Dude, who has you acting like this?!",
        "罗斯：她的笑容最美了。\n乔伊：谁的笑容美？\n罗斯：别在意啦。她的眼睛也很迷人。\n乔伊：兄弟，谁让你变成这样的？！"
    ),
    "have": (
        "Rachel: Do you **have** a pen?\nMonica: Check the drawer. I **have** lots of pens there.\nRachel: Found one! Do you **have** paper too?\nMonica: I **have** some in the desk. Help yourself!",
        "瑞秋：有笔借我用用吗？\n莫妮卡：看抽屉，那里我有好多笔。\n瑞秋：找到了！你有纸吗？\n莫妮卡：桌子里有一些。自便！"
    ),
    "he": (
        "Phoebe: Who's that guy over there?\nRachel: Oh, that's Dave. **He** works at my office.\nPhoebe: Is **He** single?\nRachel: I think so. **He** seems nice. Why? Interested?",
        "菲比：那边那个人是谁？\n瑞秋：哦，那是戴夫。他在我上班的地方工作。\n菲比：他是单身吗？\n瑞秋：应该是吧。看着不错。怎么？有兴趣？"
    ),
    "her": (
        "Ross: I saw **her** at the coffee shop today.\nRachel: Who? Sarah?\nRoss: Yeah. I couldn't stop looking at **her**.\nRachel: Ross, talk to **her**! Don't just stare at **her**!",
        "罗斯：我今天在咖啡店看到她了。\n瑞秋：谁？莎拉？\n罗斯：是啊。我忍不住一直看她。\n瑞秋：罗斯，跟她说话啊！别光盯着人家看！"
    ),
    "him": (
        "Monica: Did you see **him** at the party last night?\nRachel: Which **him**?\nMonica: **Him**! The tall guy with green shirt!\nRachel: Oh yeah! I talked to **him** for a while. He's funny!",
        "莫妮卡：昨晚派对上你看到他了吗？\n瑞秋：哪个他？\n莫妮卡：就是他啊！穿绿衬衫那个高个子！\n瑞秋：哦对！我跟他说了一会儿话。挺有趣的！"
    ),
    "his": (
        "Chandler: **His** car broke down again.\nJoey: Whose car?\nChandler: Ross's. **His** car is always breaking down.\nJoey: Maybe **His** car needs a new engine.\nChandler: Or maybe **his** driving needs improvement.",
        "钱德勒：他的车又坏了。\n乔伊：谁的车？\n钱德勒：罗斯的。他的车老是坏。\n乔伊：也许他的车需要换个发动机了。\n钱德勒：或者他的驾驶技术有待提高。"
    ),
    "how": (
        "Phoebe: **How** was your day today?\nMonica: It was okay. **How** about yours?\nPhoebe: Great! **How** do you always make such good cookies?\nMonica: It's a secret!",
        "菲比：今天过得怎么样？\n莫妮卡：还行。你呢？\n菲比：很好！你怎么总是做出这么好吃的曲奇？\n莫妮卡：秘密！"
    ),
    "if": (
        "Joey: What **if** she says yes?\nChandler: Then take her out for dinner.\nJoey: But what **if** she says no?\nChandler: Then move on. If you never ask, you'll never know!",
        "乔伊：如果她说yes怎么办？\n钱德勒：那就带她去吃饭。\n乔伊：但如果她说no呢？\n钱德勒：继续向前看。不开口就永远不知道答案！"
    ),
    "in": (
        "Monica: Rachel, are you **in** the living room?\nRachel: No, I'm **in** the kitchen!\nMonica: What are you doing **in** there?\nRachel: Making a sandwich. Want one?",
        "莫妮卡：瑞秋，你在客厅吗？\n瑞秋：不在，我在厨房！\n莫妮卡：你在那儿干嘛呢？\n瑞秋：做三明治呢。想来一个吗？"
    ),
    "is": (
        "Rachel: Where **is** everyone tonight?\nMonica: Chandler **is** working late. Joey **is** on a date.\nRachel: What about Ross? Where **is** he?\nMonica: **Is** at a museum. **He's** always somewhere nerdy.",
        "瑞秋：大家今晚都在哪？\n莫妮卡：钱德勒加班。乔伊约会去了。\n瑞秋：罗斯呢？在哪？\n莫妮卡：在博物馆。他总是在这种书呆子地方。"
    ),
    "it": (
        "Chandler: **It's** raining again!\nMonica: **It's** April. Of course **it's** raining.\nChandler: But **it** rained yesterday too!\nMonica: That's spring. **It** does what **it** wants.",
        "钱德勒：又下雨了！\n莫妮卡：现在是四月嘛。当然会下雨。\n钱德勒：但昨天下过了！\n莫妮卡：春天就是这样。想怎样就怎样。"
    ),
    "its": (
        "Ross: Look at **its** fur! So soft!\nPhoebe: What animal is this?\nRoss: It's a monkey, Marcel! Look at **its** face!\nPhoebe: Oh my god! **Its** eyes are adorable!",
        "罗斯：看它的毛！好软！\n菲比：这是什么动物？\n罗斯：猴子，马歇尔！看它的脸小小的！\n菲比：天哪！它的眼睛太可爱了！"
    ),
    "just": (
        "Rachel: I was **just** joking! Why is everyone mad?\nMonica: It wasn't funny, Rachel.\nRachel: I **just** made a tiny joke! **Just** one!\nChandler: Some things are **just** not funny.",
        "瑞秋：我只是开玩笑而已！怎么都生气？\n莫妮卡：一点都不好笑，瑞秋。\n瑞秋：我就开了个小玩笑！就一个！\n钱德勒：有些事情就是不好笑。"
    ),
    "know": (
        "Joey: You **know** what I mean?\nChandler: Yeah, I **know** exactly.\nJoey: Nobody **knows** how I feel.\nChandler: I **know**, man. I've been there.",
        "乔伊：你知道我的意思吧？\n钱德勒：知道，我完全明白。\n乔伊：没人知道我的感受。\n钱德勒：我知道，兄弟。我经历过。"
    ),
    "last": (
        "Monica: That was my **last** cookie!\nJoey: Sorry! I didn't know!\nMonica: You always eat my **last** everything! My **last** piece of cake!\nJoey: I'll buy you more! Promise!",
        "莫妮卡：那是我最后一块饼干！\n乔伊：对不起！我不知道！\n莫妮卡：你老是把我最后的东西全吃了！最后一块蛋糕也是！\n乔伊：我再给你买！保证！"
    ),
    "like": (
        "Phoebe: I really **like** your haircut!\nRachel: Thank you! Do you **like** the color too?\nPhoebe: Yeah! **Like**, the perfect shade of blonde!\nRachel: You're sweet! I **like** your honesty!",
        "菲比：我真的很喜欢你这发型！\n瑞秋：谢谢！你也喜欢这个颜色吗？\n菲比：喜欢！就像是最完美的金发颜色！\n瑞秋：你真贴心！我喜欢你的直爽！"
    ),
    "look": (
        "Rachel: **Look** at this dress! Beautiful!\nMonica: Let me **look**... wow, gorgeous!\nRachel: Should I buy it?\nMonica: **Look** at the price tag first.",
        "瑞秋：看这条裙子！美不美？\n莫妮卡：让我看看……哇，太好看了！\n瑞秋：我该买下来吗？\n莫妮卡：先看看价格标签再说。"
    ),
    "make": (
        "Monica: Let me **make** dinner tonight.\nChandler: Again? I can **make** something if you're tired.\nMonica: No, I love to **make** food for us.\nChandler: What are you going to **make**?\nMonica: Lasagna!",
        "莫妮卡：今晚让我来做晚饭吧。\n钱德勒：又来？你要是累了我可以做。\n莫妮卡：不，我喜欢给我们做饭。\n钱德勒：那你打算做什么？\n莫妮卡：千层面！"
    ),
    "me": (
        "Joey: How you doin'?\nRachel: Hi Joey. Can you help **me**?\nJoey: Anything for you! What does **me** need to do?\nRachel: Not **me** — I need YOU to move this heavy box for **me**!",
        "乔伊：你好啊？（经典搭讪）\n瑞秋：嗨乔伊。能帮我个忙吗？\n乔伊：为你什么都行！要我做什么？\n瑞秋：不是我——是我需要你来帮我搬这个重箱子！"
    ),
    "more": (
        "Chandler: I need **more** coffee.\nMonica: That's your third cup today!\nChandler: I need **more** energy! Work has been crazy!\nMonica: How about **more** sleep instead?",
        "钱德勒：我需要再来点咖啡。\n莫妮卡：这是你今天第三杯了！\n钱德勒：我需要更多精力！工作忙疯了！\n莫妮卡：少喝咖啡多睡点觉怎么样？"
    ),
    "my": (
        "Rachel: This is **my** favorite song!\nPhoebe: Mine too! Reminds **me** of summer.\nRachel: **My** mom used to play this every Sunday morning.\nPhoebe: **My** grandma used to sing it to **me** too!",
        "瑞秋：这是我最喜欢的歌！\n菲比：我也是！让我想起夏天。\n瑞秋：我妈妈以前每个周日早上都会放这首歌。\n菲比：我奶奶以前也唱给我听！"
    ),
    "new": (
        "Phoebe: Ooh, **new** shoes!\nRachel: Yeah! Bought them yesterday.\nPhoebe: They look brand **new**! Very stylish!\nRachel: Thanks! I needed something **new** for the party tonight.",
        "菲比：噢，新鞋子！\n瑞秋：对！昨天买的。\n菲比：看着像全新的！很时尚！\n瑞秋：谢谢！今晚派对我需要双新鞋子。"
    ),
    "no": (
        "Joey: **No** way! You're kidding!\nChandler: **No**, I'm serious. It happened.\nJoey: But why would he say **no**?\nChandler: Sometimes the answer's just **no**.",
        "乔伊：不可能！你在开玩笑！\n钱德勒：不，我是认真的。真发生了。\n乔伊：但为什么会拒绝？\n钱德勒：有时候答案就是不。"
    ),
    "not": (
        "Ross: This is **NOT** what I ordered!\nWaiter: I apologize, sir.\nRoss: I said **no** onions! Onions everywhere!\nRachel: Ross, calm down. It's **not** that bad.\nRoss: It IS bad! I said **NOT** onions!",
        "罗斯：这不是我点的！\n服务员：非常抱歉，先生。\n罗斯：我说不要洋葱！到处都是洋葱！\n瑞秋：罗斯，冷静点。没那么严重。\n罗斯：就很严重！我说了不要洋葱！"
    ),
    "now": (
        "Rachel: Do it **now**!\nMonica: In a minute!\nRachel: **Now**! Not later — **now**!\nMonica: Fine! Doing it **now**! Happy?\nRachel: Very!",
        "瑞秋：现在就做！\n莫妮卡：等一会儿！\n瑞秋：现在！不是以后——现在！\n莫妮卡：好吧！我现在就做！满意了？\n瑞秋：非常满意！"
    ),
    "of": (
        "Monica: Out **of** all restaurants, you picked THIS one?\nChandler: What's wrong with it?\nMonica: Nothing... out **of** all **of** them!\nChandler: I thought you'd like it. It's one **of** your favorites!",
        "莫妮卡：所有餐厅里你偏偏选这家？\n钱德勒：这家有什么问题？\n莫妮卡：没什么……那么多家里选出来的结果！\n钱德勒：我以为你会喜欢的。这不是你最爱的其中一家吗？"
    ),
    "on": (
        "Chandler: You're stepping **on** my foot!\nMonica: Am I sorry! Didn't mean to step **on** you!\nChandler: My foot was **on** the floor minding its own business!\nMonica: I'll put **on** music to make it up to you.\nChandler: Deal.",
        "钱德勒：你踩到我脚上了！\n莫妮卡：对不起！不是故意踩你的！\n钱德勒：我的脚本来安安静静放在地板上的！\n莫妮卡：我放首歌补偿你好不好？\n钱德勒：成交。"
    ),
    "one": (
        "Phoebe: **One** more song, please!\nMike: We've sung ten already!\nPhoebe: Just **one** more! Then I'll stop!\nMike: That's what you said about the last **one**!\nPhoebe: But this **one** is special!",
        "菲比：再来一首歌嘛！\n迈克：我们已经唱了十首了！\n菲比：就再来一首！然后就停！\n迈克：上一首你也这么说！\n菲比：但这首不一样！"
    ),
    "only": (
        "Ross: You're my **only** friend who understands me.\nJoey: Because I'm **only** person who listens to you!\nRoss: **Only** you, Joey.\nJoey: Just joking! You have lots of friends!",
        "罗斯：你是我唯一懂我的朋友。\n乔伊：因为只有你会听我说的话！\n罗斯：只有你了，乔伊。\n乔伊：开玩笑了啦！你有很多朋友的！"
    ),
    "or": (
        "Monica: Tea **or** coffee?\nChandler: Coffee, please. Sugar **or** cream?\nMonica: Both **or** neither?\nChandler: Both. Always both.",
        "莫妮卡：茶还是咖啡？\n钱德勒：咖啡，谢谢。加糖还是奶？\n莫妮卡：两个都要还是都不要？\n钱德勒：都要。永远都要。"
    ),
    "other": (
        "Rachel: I like this one, but the **other** one looks better.\nMonica: Which **other** one?\nRachel: The red dress over there.\nMonica: Try both on! Compare side by side.",
        "瑞秋：我喜欢这件，但另一件更好看。\n莫妮卡：哪一件？\n瑞秋：那边那条红裙子。\n莫妮卡：两件都试穿一下！并排比较。"
    ),
    "out": (
        "Joey: Let's go **out** tonight!\nChandler: Go **out** where? It's freezing.\nJoey: Go **out** for dinner! Maybe dancing!\nChandler: Fine. If we go **out**, I'm wearing my warm coat.",
        "乔伊：我们今晚出去玩吧！\n钱德勒：去哪儿玩？外面冻死人。\n乔伊：出去吃晚饭！可能再去跳舞！\n钱德勒：好吧。要出去的话我得穿暖和的外套。"
    ),
    "over": (
        "Monica: It's **over** between us!\nChandler: What? Why? It can't be **over**!\nMonica: It's **over**, Chandler!\nChandler: (pause) Is it **over** now? Can we hug?\nMonica: (hugs) It was **over** for five seconds.",
        "莫妮卡：我们之间完了！\n钱德勒：什么？为什么？不能就这样结束啊！\n莫妮卡：结束了，钱德勒！\n钱德勒：（停顿）现在结束了吗？能拥抱了吗？\n莫妮卡：（拥抱）就结束了大概五秒钟。"
    ),
    "own": (
        "Chandler: Mind your **own** business, Joey!\nJoey: Just asking! You don't need to get defensive!\nChandler: It's my **own** problem!\nJoey: Fine! Live in your **own** world then!",
        "钱德勒：管好你自己的事，乔伊！\n乔伊：我就是问问！不用这么防备！\n钱德勒：这是我自己的问题！\n乔伊：好吧！那你活在你自己的世界里吧！"
    ),
    "people": (
        "Phoebe: I love **people**! All kinds of **people**!\nRachel: Even annoying people?\nPhoebe: Especially annoying **people**! Confused souls!\nChandler: **People** who steal my sandwich are NOT confused souls. They're thieves.",
        "菲比：我爱人类！各种各样的人类！\n瑞秋：包括烦人的那种人吗？\n菲比：尤其是烦人的那种人！迷茫的灵魂！\n钱德勒：偷我三明治的人不是迷茫灵魂。他们是贼。"
    ),
    "say": (
        "Ross: **Say** something! Five minutes of silence!\nRachel: What do you want me to **say**?\nRoss: Anything! Just **say** something!\nRachel: Fine. I **say**... you need a haircut. Happy now?",
        "罗斯：说句话啊！沉默五分钟了！\n瑞秋：你说什么？\n罗斯：什么都行！就说点什么！\n瑞秋：好。我说……你需要剪头发。满意了？"
    ),
    "see": (
        "Rachel: **See** you later, guys!\nMonica: Where are you going?\nRachel: Shopping. **See** you at dinner!\nChandler: **See** ya! Don't spend too much money!\nRachel: **See** if I care! Just kidding!",
        "瑞秋：回头见各位！\n莫妮卡：你去哪？\n瑞秋：逛街。晚饭时候见！\n钱德勒：再见！别花太多钱！\n瑞秋：看我理不理你！开玩笑的！"
    ),
    "she": (
        "Monica: **She** stole my idea! Believe that?\nRachel: Who stole your idea?\nMonica: **She**! That woman from marketing!\nRachel: Calm down. **She** probably came up with it independently.\nMonica: **She** did NOT! **She's** a copycat!",
        "莫妮卡：她偷了我的想法！你能相信吗？\n瑞秋：谁偷了你的想法？\n莫妮卡：她啊！市场部那个女的！\n瑞秋：冷静点。她可能是独立想到的。\n莫妮卡：才不是！她就是个抄袭者！"
    ),
    "so": (
        "Joey: **So**... what's up, guys?\nChandler: Not much. **So** you finally showed up!\nJoey: Sorry I'm late. **So** what are we doing tonight?\nMonica: **So** glad you asked! Playing poker!",
        "乔伊：所以……各位有什么新鲜事？\n钱德勒：没什么特别的。所以你终于出现了！\n乔伊：抱歉迟到了。所以我们今晚干啥？\n莫妮卡：太高兴你问了！我们在打扑克！"
    ),
    "some": (
        "Chandler: I need **some** sleep.\nMonica: You slept eight hours!\nChandler: I need **some** more peace and quiet!\nMonica: Here's **some** advice: go to bed earlier!",
        "钱德勒：我需要睡一会儿。\n莫妮卡：你已经睡了八个小时了！\n钱德勒：我还需要更多安宁和清静！\n莫妮卡：给你个建议：今晚早点睡！"
    ),
    "something": (
        "Phoebe: There's **something** in my eye!\nRachel: Hold still. Let me check.\nPhoebe: Feels like **something** small and sharp!\nRachel: Got it! Just an eyelash. Something so tiny caused all this drama!\nPhobe: **Something** tells me I need to wash my face more.",
        "菲比：我眼睛里有东西！\n瑞秋：别动。我看看。\n菲比：感觉像是又小又尖的东西！\n瑞秋：拿出来了！就是根睫毛。这么小的东西闹这么大动静！\n菲比：有什么在提醒我得勤洗脸了。"
    ),
    "take": (
        "Ross: **Take** care of yourself while I'm gone.\nRachel: I will. You **take** care too!\nRoss: And **Take** your time with the project. Don't rush.\nRachel: Okay. **Take** it easy, Ross. Call me when you land!",
        "罗斯：我不在的时候照顾好自己。\n瑞秋：我会的。你也保重！\n罗斯：还有项目慢慢来，别着急。\n瑞秋：好的。放轻松，罗斯。落地后给我打电话！"
    ),
    "than": (
        "Monica: Nothing is more important **than** family!\nChandler: Not even your job?\nMonica: No! Family comes first — before everything else!\nChandler: Grammar aside, I feel the same. You mean more to me **than** anything!",
        "莫妮卡：没有什么比家人更重要了！\n钱德勒：连你的工作也不如？\n莫妮卡：不如！家人排在一切之前！\n钱德勒：语法错误先不说，我也这么觉得。你对我比什么都重要！"
    ),
    "that": (
        "Rachel: **That's** not fair!\nMonica: Life isn't fair.\nRachel: But **That** rule is stupid!\nMonica: **That's** the way it is. Accept and move on.",
        "瑞秋：这不公平！\n莫妮卡：生活本来就不公平。\n瑞秋：但那条规定太蠢了！\n莫妮卡：现实就是这样。接受然后往前走。"
    ),
    "the": (
        "Joey: **The** one with the hair?\nChandler: Yes, **The** Ross. The paleontologist.\nJoey: Oh, **The** Ross! Why \"The\" Ross?\nChandler: Because there's only **one** Ross. **The** world is better for it.",
        "乔伊：头发那个？（指罗斯）\n钱德勒：对，那个罗斯。那个古生物学家。\n乔伊：哦，那个罗斯！为什么叫「那个」罗斯？\n钱德勒：因为只有一个罗斯。世界因他而更美好。"
    ),
    "their": (
        "Chandler: They lost **their** way again.\nMonica: Who lost **their** way?\nChandler: Ross and Rachel. **Their** map was useless!\nMonica: Maybe **their** sense of direction is the real problem.",
        "钱德勒：他们又迷路了。\n莫妮卡：谁迷路了？\n钱德勒：罗斯和瑞秋。他们的地图根本没用！\n莫妮卡：也许是他们的方向感才是真正的问题。"
    ),
    "them": (
        "Ross: I need to talk to **them** about the divorce.\nJoey: Talk to who?\nRoss: To **them** — my ex-wife and her husband.\nJoey: Why talk to **them** together? Awkward!\nRoss: It is. But **them** understanding each other matters.",
        "罗斯：我需要和他们谈谈离婚的事。\n乔伊：和谁谈？\n罗斯：和他们——我的前妻和她现在的丈夫。\n乔伊：为什么要一起谈？很尴尬！\n罗斯：是很尴尬。但他们互相理解很重要。"
    ),
    "then": (
        "Monica: Clean the kitchen **then** watch TV.\nChandler: What happens **then**?\nMonica: **Then** relax. **Then** sleep.\nChandler: And **then**? What after **then**?\nMonica: **Then** it's tomorrow. You go to work!",
        "莫妮卡：先打扫厨房然后看电视。\n钱德勒：然后呢？\n莫妮卡：然后休息。然后睡觉。\n钱德勒：再然后呢？之后是什么？\n莫妮卡：然后就是明天了，你就去上班！"
    ),
    "there": (
        "Rachel: Over **there**! Look at that dog!\nPhoebe: Where? I don't see anything **there**.\nRachel: Right **there**! By the tree!\nPhoebe: Oh I see it now! So cute! **There** are puppies **there** too!",
        "瑞秋：在那边！看那只狗！\n菲比：哪儿？我在那边什么也没看到。\n瑞秋：就在那边！树旁边！\n菲比：哦现在看到了！好可爱！那边还有小狗崽呢！"
    ),
    "these": (
        "Phoebe: **These** flowers are beautiful!\nMonica: **These** are from my garden. I grew **them**!\nPhoebe: Really? **These** roses smell amazing!\nMonica: Take some! **These** ones here are especially nice.",
        "菲比：这些花真漂亮！\n莫妮卡：这些是我花园里的。我自己种的！\n菲比：真的吗？这些玫瑰闻着太香了！\n莫妮卡：拿一些吧！这里的这几束特别好。"
    ),
    "they": (
        "Joey: **They** don't know anything about girls!\nChandler: Who doesn't know?\nJoey: **They**! Ross and Chandler! **They** have no clue!\nMonica: Excuse me? **We** know plenty. **We** ARE girls!\nJoey: Point taken...",
        "乔伊：她们完全不懂女孩子！\n钱德勒：谁不懂？\n乔伊：她们啊！罗斯和……不对！罗斯和钱德勒！她们毫无头绪！\n莫妮卡：不好意思？我们对女孩子很了解。我们自己就是女孩子！\n乔伊：……说得有道理。"
    ),
    "thing": (
        "Chandler: **It's a thing** now! Everyone talking about it!\nMonica: What **thing**?\nChandler: You know, that **thing**! At work!\nMonica: I have no idea what **thing** you mean.\nChandler: You know — the **thing**! Never mind.",
        "钱德勒：这现在成事儿了！所有人都在讨论！\n莫妮卡：什么事儿？\n钱德勒：你知道的，那件事儿！工作上那件事儿！\n莫妮卡：我不知道你说的是什么事儿。\n钱德勒：你知道——就是那件事！算了。"
    ),
    "think": (
        "Rachel: What do you **think** about this dress?\nMonica: I **think** it's lovely!\nRachel: Really **think** so or just being nice?\nMonica: Honestly **think** it's perfect for you!",
        "瑞秋：你觉得这条裙子怎么样？\n莫妮卡：我觉得很漂亮！\n瑞秋：真的这么觉得还是在客气？\n莫妮卡：我真觉得它特别适合你！"
    ),
    "this": (
        "Ross: I love **this** city!\nRachel: **This** city? In winter?\nRoss: **This** city is magical in every season!\nRachel: Fine. But **this** street smells like garbage.\nRoss: Okay, **this** street excepted. **This** city overall is wonderful!",
        "罗斯：我爱这座城市！\n瑞秋：这座城市？冬天的时候？\n罗斯：这座城市每个季节都有魔力！\n瑞秋：好吧。但这条街闻着像垃圾堆。\n罗斯：好吧这条街除外。整座城市还是很棒的！"
    ),
    "those": (
        "Monica: Who are **those** people over there?\nChandler: **Those** guys look familiar.\nMonica: **Those** are from Ross's museum, aren't they?\nChandler: Yeah! **Those** are his coworkers. Say hi!",
        "莫妮卡：那边那些人是谁？\n钱德勒：那些家伙看着有点眼熟。\n莫妮卡：那些是罗斯博物馆的人对吧？\n钱德勒：对！那些是他的同事。过去打个招呼吧！"
    ),
    "time": (
        "Phoebe: What **time** is it?\nJoey: Almost noon! Lunch **time**!\nPhoebe: Already? **Time** flies!\nJoey: It's always **time** for food with you!",
        "菲比：几点了？\n乔伊：快中午了！午饭时间！\n菲比：已经了吗？时间过得真快！\n乔伊：对你来说什么时候都是吃饭时间！"
    ),
    "to": (
        "Rachel: Cheers! **To** friendship!\nMonica: **To** friendship! And **To** health!\nChandler: **To** not working weekends!\nJoey: **To** pizza!",
        "瑞秋：干杯！敬友谊！\n莫妮卡：敬友谊！也敬健康！\n钱德勒：敬周末不用加班！\n乔伊：敬披萨！"
    ),
    "up": (
        "Joey: What's **up**, everybody?\nChandler: Not much. What's **up** with you?\nJoey: Just woke **up**! Ready for the day!\nMonica: Someone woke **up** happy today!\nJoey: I always wake **up** happy! What's **up** for breakfast?",
        "乔伊：各位最近怎么样？\n钱德勒：没什么特别的。你怎么样？\n乔伊：刚起床！准备开始新的一天！\n莫妮卡：某人今天起床气色很好嘛！\n乔伊：每天都开心地起床！早饭吃什么？"
    ),
    "us": (
        "Ross: They're watching **us**!\nRachel: Who's watching **us**?\nRoss: Them! Over there! Staring at **us**!\nRachel: Maybe they know **us** from somewhere.\nRoss: Or maybe ignore **them** and enjoy our dinner.",
        "罗斯：他们在看着我们！\n瑞秋：谁在看我们？\n罗斯：他们啊！那边那几个！一直盯着我们！\n瑞秋：也许他们在什么地方见过我们。\n罗斯：或者我们就无视他们好好享用晚餐。"
    ),
    "very": (
        "Rachel: I'm **very** happy today!\nPhoebe: Why are you **very** happy?\nRachel: Got promoted! I'm **very** excited!\nPhoebe: That's **very** wonderful! **Very** proud of you!",
        "瑞秋：我今天很开心！\n菲比：为什么这么开心？\n瑞秋：升职了！很激动！\n菲比：真是太棒的消息！为你感到骄傲！"
    ),
    "want": (
        "Joey: I **want** pizza! Who's with me?\nChandler: We ate two hours ago!\nJoey: But I **want** pizza!\nMonica: What do you **really** **want**?\nJoey: Fine. I **want** a salad. Happy now?",
        "乔伊：我想吃披萨！谁跟我一起去？\n钱德勒：我们两小时前才吃过！\n乔伊：但我想要披萨！\n莫妮卡：你到底想要什么？\n乔伊：好吧。我想要沙拉。满意了吧？"
    ),
    "was": (
        "Monica: Where were you? I **was** worried!\nChandler: I **was** at the office late.\nMonica: Four hours? I **was** about to call the police!\nChandler: Time flew. I **was** working on a big project.",
        "莫妮卡：你去哪了？我担心死了！\n钱德勒：我在公司加班。\n莫妮卡：四个小时？我都准备报警了！\n钱德勒：时间过得快。我在做一个大项目。"
    ),
    "we": (
        "Chandler: **We** should do this more often.\nMonica: Sit around doing nothing?\nChandler: **We** work too hard. **We** need more relaxation!\nMonica: **We** can start by ordering pizza!\nChandler: Now speaking my language!",
        "钱德勒：我们应该多做这种事。\n莫妮卡：坐着什么都不干？\n钱德勒：我们工作太努力了。我们需要更多放松！\n莫妮卡：我们可以从点披萨开始！\n钱德勒：这话说到我心坎里了！"
    ),
    "well": (
        "Phoebe: **Well**, that happened.\nJoey: Didn't expect THAT!\nPhoebe: **Well**, life is full of surprises!\nJoey: **Well**, I need a drink after that!\nPhoebe: **Well**, join the club!",
        "菲比：好吧，就这样吧。\n乔伊：没想到会发生那种事！\n菲比：生活充满了意外嘛！\n乔伊：哎，聊完这个我需要喝一杯！\n菲比：哎，欢迎加入俱乐部！"
    ),
    "what": (
        "Rachel: **What**?! Are you serious?\nMonica: What's wrong?\nRachel: He said **what** to my outfit?!\nMonica: What exactly **did** he say?\nRachel: What does it matter? Whatever **what** he said was rude!",
        "瑞秋：什么？！你是认真的吗？\n莫妮卡：怎么回事？\n瑞秋：他说了我的穿着什么？！\n莫妮卡：他具体说了什么？\n瑞秋：说什么重要吗？不管说什么都很无礼！"
    ),
    "when": (
        "Ross: **When** will I see you again?\nRachel: **When** do you want to see me?\nRoss: How about **when** the sun sets tomorrow?\nRachel: Romantic. **When** did you become so poetic?\nRoss: **When** I met you.",
        "罗斯：我什么时候能再见到你？\n瑞秋：你想什么时候见？\n罗斯：明天日落时分如何？\n瑞秋：浪漫啊。你什么时候变得这么诗意的？\n罗斯：遇见你的时候。"
    ),
    "which": (
        "Monica: **Which** one should I pick? Red or blue?\nRachel: **Which** dress is for the party?\nMonica: Both! Can't decide **which** looks better.\nRachel: Wear blue. **Which** color suits your eyes more?",
        "莫妮卡：我该选哪个？红色还是蓝色？\n瑞秋：哪件裙子是派对的？\n莫妮卡：两件都是！决定不了哪个更好看。\n瑞秋：穿蓝色的吧。哪个颜色更适合你的眼睛？"
    ),
    "will": (
        "Rachel: **Will** you marry me?\nRoss: What?! **Will** I what?\nRachel: Kidding! But **Will** you help me with this report?\nRoss: Thank god. Yes, I **Will** help.",
        "瑞秋：你愿意嫁给我吗？\n罗斯：什么？！我什么意愿？\n瑞秋：开玩笑的！但你愿不愿意帮我弄这份报告？\n罗斯：谢天谢地。愿意帮你。"
    ),
    "with": (
        "Joey: I'm **with** stupid. (pointing at Chandler)\nChandler: Funny. I'm **with** genius here.\nMonica: Can you stop? I'm **with** someone who acts like a child!\nBoth: Sorry, Monica.\nMonica: Better. Who wants dinner **with** me?",
        "乔伊：我和笨蛋在一起。（指着钱德勒）\n钱德勒：好笑。我和天才在一起。\n莫妮卡：你们俩能停下吗？我和一个行为像小孩的人在一起！\n两人：对不起，莫妮卡。\n莫妮卡：这才像样。谁想跟我一起吃晚饭？"
    ),
    "would": (
        "Chandler: I **would** if I could, but can't tonight.\nMonica: What do you mean you **would**?\nChandler: I **would** love to come to dinner, but I have work.\nMonica: You always say \"I would\" but never do!\nChandler: Tonight I truly **would** if I could!",
        "钱德勒：如果我能的话我愿意，但今晚不行。\n莫妮卡：「如果我能」是什么意思？\n钱德勒：我很想去吃晚饭，但有工作。\n莫妮卡：你总是说「我愿意」但你从来不做！\n钱德勒：今晚如果真的能的话我真的愿意！"
    ),
    "year": (
        "Phoebe: It's been a great **year**!\nMike: Best **year** of my life.\nPhoebe: Every **year** with you is special.\nMike: Here's to many more **years** together!\nPhoebe: Cheers to next **year**!",
        "菲比：这是很棒的一年！\n迈克：是我人生中最棒的一年。\n菲比：和你在一起的每一年都很特别。\n迈克：敬我们一起度过的未来许多年！\n菲比：敬明年！"
    ),
    "you": (
        "Ross: I love **you**!\nRachel: **You** love me? Since **when**?\nRoss: Since forever! **You** mean everything!\nRachel: Ross... **you** have terrible timing. But I love **you** too.\nRoss: Really? **You** do?\nRachel: Yes, silly. Of course **I** do!",
        "罗斯：我爱你！\n瑞秋：你爱我？从什么时候开始的？\n罗斯：一直都是！你对我意味着一切！\n瑞秋：罗斯……你的时机选得太差了。但我也爱你。\n罗斯：真的？你爱我？\n瑞秋：是的，傻瓜。当然爱啊！"
    ),
    "your": (
        "Monica: This is **YOUR** fault, Chandler!\nChandler: How is this MY fault? It's **your** idea!\nMonica: **Your** execution was terrible!\nChandler: Fine. It's **our** fault. **Your** fault and **my** fault combined.\nMonica: That's more like it.",
        "莫妮卡：这都是你的错，钱德勒！\n钱德勒：怎么是我的错？是你的主意！\n莫妮卡：你的执行很烂！\n钱德勒：好吧。是我们的错。你的错加我的错。\n莫妮卡：这还差不多。"
    ),
}


def main():
    """升级现有词库的老友记场景"""
    print("Loading word list...")
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        words = json.load(f)
    
    updated_count = 0
    for w in words:
        word_key = w['word'].lower()
        if word_key in DIALOGUES_V1:
            new_scene, new_cn = DIALOGUES_V1[word_key]
            w['friends_scene'] = new_scene
            w['friends_cn'] = new_cn
            updated_count += 1
    
    # Save
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Updated {updated_count} / {len(words)} words with multi-turn dialogues!")
    print(f"   Total words in library: {len(words)}")


if __name__ == "__main__":
    main()
