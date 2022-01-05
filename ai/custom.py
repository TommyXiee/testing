# Title: ### D.W.G ###
# Author: ### 谢桐萌 ###
# Version: ### 1.0.0 ###
# Date: ### 04/22/2021 ###
import math
import random
import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Template Combat Turtle class.

    此AI，1.在行动模式上，采取“敌不动我动”的策略：简单来说，在对手不处于追击范围时，每隔很小一段时间随机选择一个方向来行进。
            2.在作战特性上，采取“守株待兔”的策略：对手一旦进入追击范围，此乌龟便一改不恋战的游走特性，积极展开战略行动，部署攻击。
            3.在伤害规避方面，主要以一定程度的走位来完成：设置转向速度，用于避免直线来去的弊端。
            4.此乌龟兼具隐形特性
    总体而言，此乌龟胜在行为难以预测，充满不确定性，并专精于高效的攻势。在多次与其他AI作战时收获“制敌而不自损一毫”的局面。
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        """

        ### 返回菜单中显示的名字.

        return "NewTurtle [NEW]"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str

        对乌龟AI的单行描述。返回的字符串将在游戏界面中显示
        """

        ### 描述只能有一行。

        return "evolved turtle"

    #-------------------------------------------------------------------------

    def class_shape():
        """CombatTurtle.class_shape() -> (int or tuple)
        静态方法，定义乌龟外形。



        返回整数可获得以下形状:
            0 -- 箭头 (also default in case of unrecognized index)
            1 -- 乌龟
            2 -- 犁形
            3 -- 三角形
            4 -- 筝形
            5 -- 五边形
            6 -- 六边形
            7 -- 星形
        """

        ### 可以用上文的1~7参数使用定义好的乌龟外形
        ### 也可以用数学方法返回一个元组，以自定义外形

        # return ((16, 14, 12, 14), (0, math.pi/2, math.pi, 3*math.pi/2))
        # return ((10, 10, 10, 10), (0, math.pi / 2, math.pi, 6 * math.pi / 2))
        return ((10, 10, 10, 10), (math.pi / 2, math.pi / 2, math.pi, 6 * math.pi / 2)) #隐形效果
        # return ((10, 10, 10, 10), (0, math.pi / 2, math.pi, 6 * math.pi / 2)) //一钝角三角形

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        乌龟的初始化方法.
        """

        # 定义随机方向，并重新随机化等待时间
        (self.head, self.wait) = self.rerandomize()
        self.turn_spd = 0.5 #转向速度，用于避免直线弊端
        # 定义乌龟的追击范围
        # self.pursuit_range = 0.75 * self.missile_range
        self.pursuit_range = 0.75 * self.missile_range

    # -------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        行进（步进）事件的方法。
        """

        # 重随机刷新计时器
        # self.wait -= 1
        self.wait -= 10

        # 此时间耗尽，则冲随机刷新前行方向，并重置计时器
        if self.wait <= 0:
            (self.head, self.wait) = self.rerandomize()

        # 根据与对手距离不同，决定此乌龟行为
        if (self.distance() <= self.pursuit_range
                and self.line_of_sight()):
        # if (self.distance() <= self.pursuit_range):
            # 当对手处于追击范围中时，径直冲向对手

            # 转向对手所在方向
            self.turn_towards()
            # self.left(self.turn_spd)
            # self.right(self.turn_spd)
            # Move towards opponent (or away if too close)
            if self.distance() > 2 * self.missile_radius:
                self.forward()
                self.left(self.turn_spd)
                self.right(self.turn_spd)
            else:
                self.left(self.turn_spd)
                self.right(self.turn_spd)
                self.backward()


            # 当面朝对手且对手在视线（直线）上时
            if (self.can_shoot and abs(self.relative_heading_towards()) <= 10
                    and self.line_of_sight()):
                self.shoot()

        else:
            # 当对手在追击范围之外，此乌龟随机游走

            # 转向随机的方向，并向前移动
            self.turn_towards(self.head)
            self.forward()

    # =========================================================================

    def rerandomize(self):
        """custom.rerandomize() -> tuple
        重置随机选择的方向和定时器时长。

        本乌龟采取随机游走的策略：简单来说，就是每隔一段时间随机选择一个方向来行进。
        此方法的作用是，选择一个新的随机方向，并随机化一个计时器，此计时器用于决定何时重新随机设定方向

        此方法返回一个元组（新的方向(int)，新的等待步数(int)）。
        """

        rh = random.randrange(-179, 181)  # random heading
        # rt = random.randrange(5, 31)  # random timer
        rt = random.randrange(10, 25)
        return (rh, rt)

