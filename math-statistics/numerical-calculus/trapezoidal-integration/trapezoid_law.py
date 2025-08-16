import numpy as np

def trapezoidal_rule(f, a, b, n):
    x = np.linspace(a, b, n+1)  # a에서 b까지 n+1개의 점을 생성
    y = f(x)                    # 각 점에서 함수 값 계산
    h = (b - a) / n             # 각 구간의 길이
    integral = (h / 2) * (y[0] + 2 * np.sum(y[1:n]) + y[n])  #적분 근사값 계산
    return integral

# 함수 정의
f = lambda x: x**2 + 3

# 적분 구간 및 구간 수 설정
a, b = 0, 1  # 구간설정
n = 100      # 구간 나누기

trapezoidal_result = trapezoidal_rule(f, a, b, n)
print(f"사다리꼴 법칙으로 구한 적분값: {trapezoidal_result}")
