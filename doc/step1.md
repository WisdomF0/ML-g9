# 结果分析
## 训练
![results.png](../outputs/results.png)
在十轮训练的结果中可以看到，模型的收敛情况较好，召回率也逐渐增加，如果增加训练轮数还会提高模型的准确度。
## 模型评估
![confusion_matrix_normalized](../outputs/confusion_matrix_normalized.png)
从混淆矩阵中可以看到，十轮训练得到的模型对`Bus`这一类别识别的效果较好，对`Table`识别较差
![F1_curve](../outputs/F1_curve.png)
从F1和置信度的关系曲线中，我们也可以得到同样的结论，并且从曲线中也可以看出模型还应该进一步训练。
![P_curve](../outputs/P_curve.png)
![PR_curve](../outputs/PR_curve.png)
![R_curve](../outputs/R_curve.png)
从以上三组曲线可以看出来，初步训练的模型还是比较有效的。
## 结果对比
我们抽取部分测试集的案例进行结果的对比分析<br>
真值：
![label](../outputs/val_batch2_labels.jpg)
预测：
![pred](../outputs/val_batch2_pred.jpg)
可以看到在一行四列图像的预测中，多预测出了一个`Chair`类别。在三行三列的图像中少预测出了两个`People`类别。四行三列中多预测了一个`Chair`类别。这都是由于低光照导致的。<br>
在三行四列和四行一列的多类别低光照图像中，出现了类别错误的问题，这也是由于低光照导致的图像信息不足导致的。


