
'''
Import useful packages such as Numpy, Matplotlib, Seaborn, Pandas
Define utility functions:

plot_missing
plot_corr
plot_unique
plot_distribution

'''
# 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import itertools

# sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso

def plot_missing(df):

    fig, ax = plt.subplots(figsize = (15,8))
    miss = df.apply(lambda x: x.isnull().sum() / len(df)).sort_values(ascending = False)

    # Formatting ax
    ax = sns.barplot(y = miss.values, x = miss.index)

    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2%'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 10), 
                    textcoords = 'offset points')

    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45)
    ax.set_ylim(0,1)  
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel('Percentage of Missing')

    # formatting ax2
    ax2 = ax.twinx()
    ax2.set_ylim(0, len(df))
    ax2.set_ylabel('Count of Missing')

    # Use a MultipleLocator to ensure a tick spacing of 10
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(10000))
    ax2.set_yticklabels(['{:,.0f}K'.format(x/1000) for x in ax2.get_yticks()])

    plt.title('Missing Value')
    fig.tight_layout()
    sns.despine()
    plt.show()

def plot_corr(df, figsize):
    '''
    This function plots the correlation plot between numeric variables
    
    '''
    corr = df.select_dtypes(['float64', 'int64']).corr()
    
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype = np.bool)
    
    mask[np.triu_indices_from(mask)] = True
    
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize = figsize)
    
    # Generate a custome diverging colormap
    cmap = sns.diverging_palette(220, 10 , as_cmap = True)
    
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask = mask, cmap = cmap, vmax = 1, vmin = -1, center = 0,
               square = True, linewidths = 0.5, cbar_kws = {'shrink':0.5})
    
    plt.title('Correlation Plot of Numeric Variables')
    
    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_unique(df, col, show_count = False, show_percent = False, fontsize = 15, figsize = (15,8), hue = None): 
    
    fig, ax = plt.subplots(figsize = figsize)
    
    ax = sns.countplot(x = col, hue = hue, data = df)
    
    # show exact number on each bar
    if show_count:
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 10), 
                        textcoords = 'offset points')
    else:
        pass
    
    # show percentages on each bar
    if show_percent:
        bars = ax.patches
        half = int(len(bars)/2)
        left_bars = bars[:half]
        right_bars = bars[half:]

        for left, right in zip(left_bars, right_bars):
            height_l = left.get_height()
            height_r = right.get_height()
            total = height_l + height_r

            ax.text(left.get_x() + left.get_width()/2., height_l + 200, '{0:.0%}'.format(height_l/total), ha="center")
            ax.text(right.get_x() + right.get_width()/2., height_r + 200, '{0:.0%}'.format(height_r/total), ha="center")
    else:
        pass

    ax.set_title('{} Count distribution'.format(col), fontsize = fontsize)
    
    if hue != None:
         plt.legend(loc = 'upper right', frameon = False)
    else:
        pass
    
    fig.tight_layout()
    sns.despine()
    plt.show()

def plot_distribution(df, col, target, figsize = (15,8)):
    
    fig, axes = plt.subplots(nrows = 2, figsize = figsize)
    
    for _ in sorted(df[target].unique().tolist()):
        sns.distplot(df[df[target] == _][col], hist = True, rug = False, label = _)
    
    ax = sns.boxplot(x = target, y = col, data = df, ax = axes[0])
    
    plt.legend(loc = 'upper right', frameon = False)
    ax.set_title('distribution of {} by response group'.format(col))
    
    fig.tight_layout()
    sns.despine(left = True)
    plt.show()

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

def show_data(cm, print_res = 0):
    tp = cm[1,1]
    fn = cm[1,0]
    fp = cm[0,1]
    tn = cm[0,0]
    if print_res == 1:
        print('Precision =     {:.3f}'.format(tp/(tp+fp)))
        print('Recall (TPR) =  {:.3f}'.format(tp/(tp+fn)))
        print('Fallout (FPR) = {:.3f}'.format(fp/(fp+tn)))
    return tp/(tp+fp), tp/(tp+fn), fp/(fp+tn)

def plot_roc(X_test, y_test, algo):
    '''
    This function plots the ROC curve for an algorithm
    
    '''
    probs = algo.predict_proba(X_test)
    preds = probs[:,1]
    fpr, tpr, threshold = roc_curve(y_test, preds)
    roc_auc = auc(fpr, tpr)

    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.4f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()

def plot_confusion(thresh, algo):
    ''' 
    This function plot the confusion matrix
    
    '''
    probs = algo.predict_proba(X_test)
    y_pred = [1 if x > thresh else 0 for x in probs[:,1]]
    cm = confusion_matrix(y_test, y_pred)
    plot_confusion_matrix(cm, ['0', '1'], )
    pr, tpr, fpr = show_data(cm, print_res = 1)


def plot_importance(X, algo, num_feature_show):
    '''
    This function plot the feature importance for random forest algorithm
    
    '''
    import pandas as pd
    
    impor = pd.DataFrame({
        'feature': X.columns,
        'importance': algo.feature_importances_
    })
    
    impor = impor.sort_values('importance', ascending = False)
    
    fig, axes = plt.subplots(figsize = (15,8))
    sns.barplot(y = 'feature', x = 'importance', data = impor.iloc[:num_feature_show,:])
    
    # plt.xticks(rotation = 90)
    plt.title('Feature Importance')
    
    sns.despine()
    plt.tight_layout()
    plt.show()