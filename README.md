# Orlo
A guided tour of ROC curves

![Orlo Touring Car](https://github.com/rebeccabilbro/orlo/blob/master/figures/orlo_touring_car.jpg)    
From [Public Domain Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/9/9c/Orlo_Touring_Car.jpg)

A receiver operating characteristic (ROC) curve is a graph that illustrates the performance of a binary classifier system as its discrimination threshold is varied. The curve is created by plotting the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings. The true-positive rate is also known as *sensitivity*, or **recall** in machine learning. The false-positive rate is also known as the fall-out and can be calculated as (1 - specificity). The ROC curve is thus the sensitivity as a function of fall-out. In general, if the probability distributions for both detection and false alarm are known, the ROC curve can be generated by plotting the cumulative distribution function (area under the probability distribution from -infinity to +infinity) of the detection probability in the y-axis versus the cumulative distribution function of the false-alarm probability in x-axis.

ROC analysis provides tools to select possibly optimal models and to discard suboptimal ones independently from (and prior to specifying) the cost context or the class distribution. ROC analysis is related in a direct and natural way to cost/benefit analysis of diagnostic decision making.

The ROC curve was first developed by electrical engineers and radar engineers during World War II for detecting enemy objects in battlefields and was soon introduced to psychology to account for perceptual detection of stimuli. ROC analysis since then has been used in medicine, radiology, biometrics, and other areas for many decades and is increasingly used in machine learning and data mining research.

The ROC is also known as a relative operating characteristic curve, because it is a comparison of two operating characteristics (TPR and FPR) as the criterion changes.

[Wikipedia entry on ROC curves](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)

## Recommended Reading    
[Fawcett, Tom. "An introduction to ROC analysis."Pattern recognition letters 27.8 (2006): 861-874.](https://ccrma.stanford.edu/workshops/mir2009/references/ROCintro.pdf)

In Python, a basic template for plotting ROC curves using `scikit-learn` and `matplotlib` would be:

```python
import matplotlib.pyplot as plt
from sklearn.metrics import auc
from sklearn.metrics import roc_curve

actual       =  [0,0,1,0,0,0,1,0,0,1,1,1,1,0]
predictions  =  [0.1,0,1,0,0,0.3,1,0,0,.9,1,1,1,0.1]

false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predictions)
roc_auc = auc(false_positive_rate, true_positive_rate)

plt.title('Receiver Operating Characteristic')
plt.plot(false_positive_rate, true_positive_rate, 'blue', label='AUC = %0.2f'% roc_auc)
plt.legend(loc='lower right')
plt.plot([0,1],[0,1],'m--')
plt.xlim([0,1])
plt.ylim([0,1.1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
```

Also easily implemented in R:

```R
install.packages("ROCR")
library(ROCR)

actual <- c(0,0,1,0,0,0,1,0,0,1,1,1,1,0)
predictions <- c(0.1,0,1,0,0,0.3,1,0,0,.9,1,1,1,0.1)

ROCRpred <- prediction(predictions,actual)
plot(performance(ROCRpred, measure = 'tpr', x.measure = 'fpr'), col="blue", xlab='False Positive Rate', ylab='True Positive Rate', main='Receiver Operating Characteristic', xaxs="i")
abline(a=0, b=1, lty=2, col="purple")

auc.perf = performance(ROCRpred, measure = "auc")
aucvalue <- paste(c("AUC  = "), auc.perf@y.values, sep="")
legend(0.7, y=0.2, aucvalue, bty='n', lty=1, col="blue")
```
