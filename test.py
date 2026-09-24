import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Seaborn-এর built-in ডেটাসেট লোড
titanic = sns.load_dataset('titanic')

# ডেটার প্রথম কয়েক লাইন দেখা
print(titanic.head())

# ক্লাস অনুযায়ী বেঁচে থাকার সংখ্যা
sns.countplot(data=titanic, x='class', hue='survived')
plt.title('ক্লাস অনুযায়ী বেঁচে থাকার হার')
plt.show()

# বয়সের বন্টন
sns.histplot(data=titanic, x='age', bins=30, kde=True)
plt.title('যাত্রীদের বয়স বন্টন')
plt.show()