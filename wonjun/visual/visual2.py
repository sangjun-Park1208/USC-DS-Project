# import matplotlib.pyplot as plt
# import numpy as np
#
# # degree와 average cross-validation score의 리스트
# degrees = [2, 3, 4, 5]
# avg_cross_val_scores = [-9.302109645469654, -13.59482450790027, -13.702999954989272, -329.26082303838115]
#
# # 막대 그래프를 그리기 위해 degree를 범주로, 그에 대응하는 cross_val_score를 값으로 설정
# plt.bar(degrees, [-1*np.log(-x) for x in avg_cross_val_scores])  # Use the log scale manually on y-axis because the bar plot doesn't support it directly
#
# # 그래프에 제목 및 x, y 축 레이블 추가
# plt.title('Average Cross-Validation Score vs Degree')
# plt.xlabel('Degree')
# plt.ylabel('Average Cross-Validation Score (Log Scale)')
#
# # 그래프를 표시
# plt.savefig('1', dpi=600)
# plt.show()

import matplotlib.pyplot as plt

# degree와 average cross-validation score의 리스트
degrees = [2, 3, 4, 5]
avg_cross_val_scores = [-9.302109645469654, -13.59482450790027, -13.702999954989272, -329.26082303838115]

# 막대 그래프를 그리기 위해 degree를 범주로, 그에 대응하는 cross_val_score를 값으로 설정
# width를 0.4로 설정하여 막대 너비를 절반으로 줄임
bars = plt.bar(degrees, avg_cross_val_scores, width=0.4)

# 그래프에 제목 및 x, y 축 레이블 추가
plt.title('Average Cross-Validation Score vs Degree')
plt.xlabel('Degree')
plt.ylabel('Average Cross-Validation Score')

# x축 레이블을 상단으로 이동
plt.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)

# x축에 정수만 표시되도록 xticks 설정
plt.xticks(ticks=degrees)

# 그래프를 표시
plt.savefig('2', dpi=600)
plt.show()



