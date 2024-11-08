import math
from typing import List, Union # 添加类型注解

# 节点类
class Node:
    """
    表示 数值/中间操作 的数据结果
    """
    init_id = -1 # 初始化节点的ID
    def __init__(self, op:'Op', inputs:List[Union[float,'Node']]):
        self.op = op
        self.inputs = inputs
        self.grad = 0.0 # 初始化梯度为0
        self.evaluate() # 计算当前节点的值

        # 调试信息
        self.id = Node.init_id
        Node.init_id += 1
        print(self)

    def input_values(self):
        """
        将输入转换成数值，**具体的计算只能发生在数值上**
        """
        return [i.value if isinstance(i, Node) else i for i in self.inputs]
    
    def evaluate(self):
        """ 
        计算当前节点的值
        """
        self.value = self.op.compute(self.input_values())
        
    def __repr__(self):
        return self.__str__()
    # repr 和 str 内置方法
    def __str__(self):
        return f'Node {self.id} : {self.input_values()} {self.op.name} = {self.value}, and grad: {self.grad:.3f}'

# 操作类
class Op:
    """
    所有操作的基类

    注意：这个类不能直接使用，只能用于继承
        这个类本身不包含状态，计算的状态保存在 Node 中，每次调用都会产生一个 Node 对象
    每次执行操作时，都会生成一个新的Node节点，该节点保存了操作的输入、输出以及梯度信息。
    """
    def name(self):
        """返回操作的名称"""
        pass

    def __call__(self):
        """
        生成一个新的 Node 对象
            实例化操作对象后通过 () 调用时触发
        """
        pass
    
    def compute(self, inputs:List[Union[float,Node]]):
        """ 
        计算操作的结果
        """
        pass
    def gradient(self, output_grad:float):
        """
        计算梯度
        """
        pass
class AddOp(Op):
    """ 
    加法操作
    """
    def name(self):
        return 'Add'
    def __call__(self, lhs:Union[float,Node], rhs:Union[float,Node]):
        return Node(self, [lhs, rhs])
    def compute(self, inputs:List[Union[float,Node]]):
        return inputs[0] + inputs[1]
    def gradient(self, output_grad:float):
        return [output_grad, output_grad] # rhs 和 lhs 的梯度

class SubOp(Op):
    """ 
    减法操作
    """
    def name(self):
        return 'Sub'
    def __call__(self, lhs:Union[float,Node], rhs:Union[float,Node]):
        return Node(self, [lhs, rhs])
    def compute(self, inputs:List[Union[float,Node]]):
        return inputs[0] - inputs[1]
    def gradient(self, output_grad:float):
        return [output_grad, -output_grad]


    
        
    