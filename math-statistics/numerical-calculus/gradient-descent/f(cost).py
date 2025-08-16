import numpy as np
import matplotlib.pyplot as plt

# 데이터 생성 (예시)
np.random.seed(42)
X = 4 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# X0 = 1 추가 (바이어스 항)
X_b = np.c_[np.ones((100, 1)), X]

# 초기 매개변수 설정
theta = np.random.randn(2, 1)

# 비용 함수 (MSE) 계산 함수
def compute_cost(X, y, theta):
    m = len(y)
    predictions = X.dot(theta)
    cost = (1/(2*m)) * np.sum((predictions - y)**2)
    return cost

# 경사 하강법 함수
def gradient_descent(X, y, theta, learning_rate, iterations):
    m = len(y)
    cost_history = []
    
    for iteration in range(iterations):
        gradients = (1/m) * X.T.dot(X.dot(theta) - y)
        theta = theta - learning_rate * gradients
        cost = compute_cost(X, y, theta)
        cost_history.append(cost)
    
    return theta, cost_history

# 하이퍼파라미터 설정
learning_rate = 0.1
iterations = 100

# 경사 하강법 수행
theta, cost_history = gradient_descent(X_b, y, theta, learning_rate, iterations)

# 비용 함수 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(range(iterations), cost_history, marker='o')
plt.title('Cost Function over Iterations')
plt.xlabel('Iterations')
plt.ylabel('Cost (MSE)')
plt.grid(True)
plt.show()
