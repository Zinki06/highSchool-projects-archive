import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from skimage import io, metrics
from skimage.restoration import denoise_tv_chambolle
from skimage.util import random_noise, img_as_float


def gradient_descent_example(save_path=None):
    """경사하강법을 이용한 선형회귀 최적화"""
    print("=== 경사하강법 선형회귀 ===")
    
    # 데이터 생성
    np.random.seed(42)
    X = 4 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)
    X_b = np.c_[np.ones((100, 1)), X]  # 바이어스 항 추가
    
    # 초기 매개변수
    theta = np.random.randn(2, 1)
    learning_rate = 0.1
    iterations = 100
    
    # 비용 함수 계산
    def compute_cost(X, y, theta):
        m = len(y)
        predictions = X.dot(theta)
        cost = (1/(2*m)) * np.sum((predictions - y)**2)
        return cost
    
    # 경사하강법 수행
    cost_history = []
    for i in range(iterations):
        gradients = (1/len(y)) * X_b.T.dot(X_b.dot(theta) - y)
        theta = theta - learning_rate * gradients
        cost = compute_cost(X_b, y, theta)
        cost_history.append(cost)
    
    print(f"최종 매개변수: θ₀={theta[0][0]:.2f}, θ₁={theta[1][0]:.2f}")
    print(f"최종 비용: {cost_history[-1]:.4f}")
    
    # 시각화
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 데이터와 회귀선
    ax1.scatter(X, y, alpha=0.6)
    X_plot = np.linspace(0, 4, 100)
    y_plot = theta[0] + theta[1] * X_plot
    ax1.plot(X_plot, y_plot, 'r-', linewidth=2, label=f'y = {theta[0][0]:.2f} + {theta[1][0]:.2f}x')
    ax1.set_xlabel('X')
    ax1.set_ylabel('y')
    ax1.set_title('Linear Regression Result')
    ax1.legend()
    ax1.grid(True)
    
    # 비용 함수 수렴
    ax2.plot(range(iterations), cost_history, 'b-', linewidth=2)
    ax2.set_xlabel('Iterations')
    ax2.set_ylabel('Cost (MSE)')
    ax2.set_title('Cost Function Convergence')
    ax2.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"결과 저장: {save_path}")
    
    plt.show()
    
    return cost_history


def trapezoidal_integration(save_path=None):
    """사다리꼴 공식을 이용한 수치 적분"""
    print("\n=== 사다리꼴 적분법 ===")
    
    def f(x):
        return x**2 + 3
    
    def trapezoidal_rule(func, a, b, n):
        """사다리꼴 공식 구현"""
        h = (b - a) / n
        x = np.linspace(a, b, n+1)
        y = func(x)
        integral = (h / 2) * (y[0] + 2 * np.sum(y[1:n]) + y[n])
        return integral, x, y
    
    # 적분 계산
    a, b = 0, 2
    n_values = [10, 50, 100, 500]
    
    # 정확한 값 (해석적 해)
    exact_value = (2**3/3 + 3*2) - (0**3/3 + 3*0)
    print(f"정확한 적분값: {exact_value:.6f}")
    
    plt.figure(figsize=(12, 8))
    
    for i, n in enumerate(n_values):
        result, x, y = trapezoidal_rule(f, a, b, n)
        error = abs(result - exact_value)
        
        print(f"n={n:3d}: 근사값={result:.6f}, 오차={error:.6f}")
        
        # 시각화
        plt.subplot(2, 2, i+1)
        x_smooth = np.linspace(a, b, 200)
        y_smooth = f(x_smooth)
        plt.plot(x_smooth, y_smooth, 'b-', linewidth=2, label=f'f(x) = x² + 3')
        
        # 사다리꼴 표시
        for j in range(len(x)-1):
            plt.fill_between([x[j], x[j+1]], [0, 0], [y[j], y[j+1]], 
                           alpha=0.3, color='red')
        
        plt.title(f'n = {n}, Error = {error:.6f}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True)
        plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"결과 저장: {save_path}")
    
    plt.show()


def image_denoising_demo(save_path=None):
    """이미지 디노이징 데모"""
    print("\n=== 이미지 디노이징 ===")
    
    # 샘플 이미지 경로
    image_path = "Image denoising/IMG_1938.JPG"
    
    if not os.path.exists(image_path):
        print("샘플 이미지를 찾을 수 없음. 간단한 합성 이미지로 대체함")
        # 간단한 테스트 이미지 생성
        original = np.zeros((100, 100))
        original[25:75, 25:75] = 1.0
        original[40:60, 40:60] = 0.5
    else:
        original = img_as_float(io.imread(image_path, as_gray=True))
        print(f"이미지 로드 완료: {original.shape}")
    
    # 노이즈 추가
    noise_var = 0.1
    noisy = random_noise(original, mode='gaussian', var=noise_var)
    print(f"가우시안 노이즈 추가 (분산: {noise_var})")
    
    # Total Variation 디노이징
    denoised = denoise_tv_chambolle(noisy, weight=0.1)
    
    # 성능 지표 계산
    if original.max() > 0:
        psnr = metrics.peak_signal_noise_ratio(original, denoised, data_range=1.0)
        ssim = metrics.structural_similarity(original, denoised, data_range=1.0)
        print(f"PSNR: {psnr:.2f}dB")
        print(f"SSIM: {ssim:.3f}")
    
    # 시각화
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(original, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    axes[1].imshow(noisy, cmap='gray')
    axes[1].set_title('Noisy Image')
    axes[1].axis('off')
    
    axes[2].imshow(denoised, cmap='gray')
    axes[2].set_title('Denoised Image')
    axes[2].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"결과 저장: {save_path}")
    
    plt.show()


def energy_convergence_analysis(save_path=None):
    """Total Variation 에너지 함수 수렴 분석"""
    print("\n=== 에너지 함수 수렴 분석 ===")
    
    # 간단한 테스트 이미지
    original = np.zeros((50, 50))
    original[15:35, 15:35] = 1.0
    
    # 노이즈 추가
    noisy = random_noise(original, mode='gaussian', var=0.1)
    
    # 반복적 디노이징으로 에너지 변화 관찰
    def compute_tv_energy(image, lambda_val=0.1):
        """Total Variation 에너지 계산"""
        grad_x = np.gradient(image, axis=0)
        grad_y = np.gradient(image, axis=1)
        tv_term = np.sum(np.sqrt(grad_x**2 + grad_y**2))
        data_term = np.sum((image - original)**2)
        return data_term + lambda_val * tv_term
    
    energies = []
    current_image = noisy.copy()
    
    for i in range(20):
        energy = compute_tv_energy(current_image)
        energies.append(energy)
        
        if i < 19:  # 마지막 반복이 아니면 디노이징 적용
            current_image = denoise_tv_chambolle(current_image, weight=0.1)
    
    print(f"초기 에너지: {energies[0]:.2f}")
    print(f"최종 에너지: {energies[-1]:.2f}")
    print(f"에너지 감소: {energies[0] - energies[-1]:.2f}")
    
    # 에너지 수렴 시각화
    plt.figure(figsize=(10, 6))
    plt.plot(range(20), energies, 'o-', linewidth=2, markersize=6)
    plt.xlabel('Iterations')
    plt.ylabel('Total Variation Energy')
    plt.title('Energy Function Convergence')
    plt.grid(True)
    plt.yscale('log')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"결과 저장: {save_path}")
    
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='미적분학 응용 프로그램')
    parser.add_argument('--mode', '-m', choices=['all', 'gradient', 'integral', 'denoise', 'energy'], 
                       default='all', help='실행할 모드 선택')
    parser.add_argument('--save-results', action='store_true', 
                       help='결과 이미지를 results 폴더에 저장')
    
    args = parser.parse_args()
    
    # results 폴더 생성
    if args.save_results:
        os.makedirs('results', exist_ok=True)
    
    print("미적분학 응용 프로그램")
    print("=" * 50)
    
    if args.mode in ['all', 'gradient']:
        gradient_descent_example(save_path='results/gradient_descent_result.png' if args.save_results else None)
    
    if args.mode in ['all', 'integral']:
        trapezoidal_integration(save_path='results/trapezoidal_integration.png' if args.save_results else None)
    
    if args.mode in ['all', 'denoise']:
        image_denoising_demo(save_path='results/image_denoising_comparison.png' if args.save_results else None)
    
    if args.mode in ['all', 'energy']:
        energy_convergence_analysis(save_path='results/energy_convergence.png' if args.save_results else None)
    
    print("\n실행 완료!")


if __name__ == '__main__':
    main()