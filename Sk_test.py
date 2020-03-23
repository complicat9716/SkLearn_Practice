import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import svm



# load data set
digits = datasets.load_digits()

# example
print('all the datas: ')
print(digits.data[0])          # all the datas
print(len(digits.data))
print('target set: ')
print(digits.target)        # target numbers
print(len(digits.target))
print('first image: ')
print(digits.images[0])     # first image

# # plot the first image
# plt.gray()
# plt.title('first number image')
# plt.imshow(digits.images[0])
# plt.show()


# machine learning
clf = svm.SVC(gamma=0.001, C=100)

x, y = digits.data[:-10], digits.target[:-10]
clf.fit(x, y)

print('Prediction: ', clf.predict(digits.data[[-2]]))

# show actual image
plt.imshow(digits.images[-2], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()
