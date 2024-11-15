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

    def input_values(self) -> List[float]:
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
    def __str__(self) -> str:
        return f'Node {self.id} : {self.input_values()} {self.op.name()} = {self.value}, and grad: {self.grad:.3f}'

# 操作类
class Op:
    """
    所有操作的基类

    注意：这个类不能直接使用，只能用于继承
        这个类本身不包含状态，计算的状态保存在 Node 中，每次调用都会产生一个 Node 对象
    每次执行操作时，都会生成一个新的Node节点，该节点保存了操作的输入、输出以及梯度信息。
    """
    def name(self) -> str:
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
    def gradient(self, output_grad:float) -> List[float]:
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
    def gradient(self,inputs:List[Union[float, Node]], output_grad:float):
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
    def gradient(self,inputs:List[Union[float, Node]], output_grad:float):
        return [output_grad, -output_grad]

class MulOp(Op):
    """ 
    乘法操作
    """
    def name(self):
        return 'Mul'
    def __call__(self, lhs:Union[float,Node], rhs:Union[float,Node]):
        return Node(self, [lhs, rhs])
    def compute(self, inputs:List[Union[float,Node]]):
        return inputs[0] * inputs[1]
    def gradient(self, inputs:List[Union[float,Node]], output_grad:float):
        return [inputs[1] * output_grad, inputs[0] * output_grad]

class LnOp(Op):
    """ 
    对数操作
    """
    def name(self):
        return 'Ln'
    def __call__(self, x:Union[float,Node]):
        return Node(self, [x])
    def compute(self, inputs:List[Union[float,Node]]):
        return math.log(inputs[0])
    def gradient(self, inputs:List[Union[float,Node]], output_grad:float):
        return [1.0 * output_grad / inputs[0]]
class SinOp(Op):
    """ 
    正弦操作
    """
    def name(self):
        return 'Sin'
    def __call__(self, x:Union[float,Node]):
        return Node(self, [x])
    def compute(self, inputs:List[Union[float,Node]]):
        return math.sin(inputs[0])
    def gradient(self, inputs:List[Union[float,Node]], output_grad:float):
        return [math.cos(inputs[0]) * output_grad]
class IdentityOp(Op):
    """ 
    恒等操作
    """
    def name(self):
        return 'Identity'
    def __call__(self, x:Union[float,Node]):
        return Node(self, [x])
    def compute(self, inputs:List[Union[float,Node]]):
        return inputs[0]
    def gradient(self,inputs:List[Union[float, Node]],  output_grad:float):
        return [output_grad]


class Executor():
    """ 执行器 """
    def __init__(self, root:'Node'):
        self.root = root
        self.topo_list = self.__topo_sort(root)
    def __topo_sort(self, root:'Node'):
        """
        拓扑排序
        """
        visited = set()
        topo_list = []
        def dfs(node:'Node'):
            if node in visited:
                return
            visited.add(node)
            for n in node.inputs:
                if isinstance(n, Node):
                    dfs(n)
            topo_list.append(node)
        dfs(root)
        return topo_list
    
    def gradients(self) -> None:
        """
        计算梯度
        """
        reverse_topo_list:List[Node] = self.topo_list[::-1] # 反向微分
        reverse_topo_list[0].grad = 1.0 # 设置输出节点的梯度为1
        for node in reverse_topo_list:
            grad = node.op.gradient(node.input_values(), node.grad)
            # 将梯度累加到每一个输入变量的梯度上
            for n, g in zip(node.inputs, grad):
                if isinstance(n, Node):
                    n.grad += g
        print('Gradients computed:\n\n')
        for node in reverse_topo_list:
            print(node)
    def run(self):
        """
        按照拓扑排序的顺序对计算图求值。        
        """
        visited = set()
        print('Evaluation order:')
        for node in self.topo_list:
            if node not in visited:
                node.evaluate()
                visited.add(node)
                print("evaluating node: ", node)
        return self.root.value
