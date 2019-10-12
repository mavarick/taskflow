### 说明

taskflow主要说明了一种程序流，就像本身所说，很多个子任务合并起来完成一个任务，这个任务可能需要多个输出，可能需要多个并行，可能需要多个输入等等，而taskflow就可以完成这样的需求。

![taskflow](https://github.com/mavarick/taskflow/blob/master/files/taskflow.jpg)

通过分解任务，并且组合各种不同的tasks，可以完成代码的各种粒度级别的重用。

#### 仍需要做的

- [] 加入signal信号，进行控制。
- [] 增加各种tasks。
- [] 对task的初始化和析构的处理。
