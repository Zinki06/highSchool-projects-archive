"""
이미지 디노이징 알고리즘 비교 도구
Total Variation vs Bilateral 필터 성능 분석
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import argparse
import os
import platform
from skimage import io, metrics
from skimage.restoration import denoise_tv_chambolle, denoise_bilateral
from skimage.util import random_noise, img_as_float


def setup_korean_font():
    """한글 폰트 설정"""
    try:
        system = platform.system()
        if system == 'Darwin':  # macOS
            font_names = ['AppleGothic', 'Noto Sans CJK KR']
        elif system == 'Windows':
            font_names = ['Malgun Gothic', 'NanumGothic']
        else:  # Linux
            font_names = ['Noto Sans CJK KR', 'DejaVu Sans']
        
        for font_name in font_names:
            try:
                plt.rcParams['font.family'] = font_name
                return True
            except:
                continue
        
        plt.rcParams['font.family'] = 'sans-serif'
        return False
    except:
        plt.rcParams['font.family'] = 'sans-serif'
        return False


def load_image(path):
    """이미지 불러오기"""
    if not os.path.exists(path):
        print(f"파일 없음: {path}")
        return None
    return img_as_float(io.imread(path))


def add_gaussian_noise(image, variance=0.01):
    """가우시안 노이즈 추가"""
    return random_noise(image, mode='gaussian', var=variance)


def total_variation_denoise(noisy_image, weight=0.1):
    """Total Variation 디노이징"""
    return denoise_tv_chambolle(noisy_image, weight=weight)


def bilateral_denoise(noisy_image, sigma_color=0.05, sigma_spatial=15):
    """Bilateral 필터 디노이징"""
    return denoise_bilateral(noisy_image, sigma_color=sigma_color, sigma_spatial=sigma_spatial)


def calculate_psnr(original, processed):
    """PSNR 계산"""
    return metrics.peak_signal_noise_ratio(original, processed)


def calculate_ssim(original, processed):
    """SSIM 계산"""
    channel_axis = -1 if len(original.shape) == 3 else None
    return metrics.structural_similarity(original, processed, channel_axis=channel_axis, data_range=1.0)


def energy_function(u, f, lambda_val=0.1):
    """TV 에너지 함수 계산"""
    data_term = np.sum((u - f)**2)
    
    if len(u.shape) == 3:
        grad_u_x = np.gradient(u, axis=0)
        grad_u_y = np.gradient(u, axis=1)
        reg_term = np.sum(np.sqrt(grad_u_x**2 + grad_u_y**2))
    else:
        grad_u = np.gradient(u)
        reg_term = np.sum(np.sqrt(grad_u[0]**2 + grad_u[1]**2))
    
    return data_term + lambda_val * reg_term


def show_comparison_results(original, noisy, tv_result, bilateral_result, save_path=None):
    """알고리즘 비교 결과 시각화"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0,0].imshow(original, cmap='gray' if len(original.shape) == 2 else None)
    axes[0,0].set_title('원본 이미지')
    axes[0,0].axis('off')
    
    axes[0,1].imshow(noisy, cmap='gray' if len(noisy.shape) == 2 else None)
    axes[0,1].set_title('노이즈 이미지')
    axes[0,1].axis('off')
    
    # TV 결과
    tv_psnr = calculate_psnr(original, tv_result)
    tv_ssim = calculate_ssim(original, tv_result)
    axes[1,0].imshow(tv_result, cmap='gray' if len(tv_result.shape) == 2 else None)
    axes[1,0].set_title(f'Total Variation\nPSNR: {tv_psnr:.2f}dB, SSIM: {tv_ssim:.3f}')
    axes[1,0].axis('off')
    
    # Bilateral 결과
    bil_psnr = calculate_psnr(original, bilateral_result)
    bil_ssim = calculate_ssim(original, bilateral_result)
    axes[1,1].imshow(bilateral_result, cmap='gray' if len(bilateral_result.shape) == 2 else None)
    axes[1,1].set_title(f'Bilateral Filter\nPSNR: {bil_psnr:.2f}dB, SSIM: {bil_ssim:.3f}')
    axes[1,1].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"결과 저장: {save_path}")
    
    plt.show()


def analyze_convergence(original, noisy, max_iter=10, save_path=None):
    """TV 알고리즘 수렴 분석"""
    energies = []
    psnr_values = []
    current_image = noisy.copy()
    
    for i in range(max_iter + 1):
        if i > 0:
            current_image = denoise_tv_chambolle(current_image, weight=0.1)
        
        energy = energy_function(current_image, original)
        psnr = calculate_psnr(original, current_image)
        
        energies.append(energy)
        psnr_values.append(psnr)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    iterations = np.arange(max_iter + 1)
    ax1.plot(iterations, energies, 'o-', color='blue')
    ax1.set_title('에너지 함수 수렴')
    ax1.set_xlabel('반복 횟수')
    ax1.set_ylabel('에너지')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    ax2.plot(iterations, psnr_values, 's-', color='red')
    ax2.set_title('PSNR 개선 과정')
    ax2.set_xlabel('반복 횟수')
    ax2.set_ylabel('PSNR (dB)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"수렴 분석 저장: {save_path}")
    
    plt.show()
    return energies, psnr_values


def main():
    parser = argparse.ArgumentParser(description='이미지 디노이징 알고리즘 비교')
    parser.add_argument('--input', '-i', default='sample.jpg',
                       help='입력 이미지 경로')
    parser.add_argument('--output', '-o', default='results/',
                       help='결과 저장 경로')
    parser.add_argument('--noise', '-n', type=float, default=0.01,
                       help='노이즈 분산 (기본값: 0.01)')
    parser.add_argument('--convergence', '-c', action='store_true',
                       help='수렴 분석 실행')
    
    args = parser.parse_args()
    
    # 한글 폰트 설정
    font_ok = setup_korean_font()
    if not font_ok:
        print("⚠ 한글 폰트 미지원")
    
    # 이미지 로드
    original_image = load_image(args.input)
    if original_image is None:
        print("기본 샘플 이미지 생성")
        # 간단한 테스트 이미지 생성
        original_image = np.zeros((100, 100))
        original_image[20:80, 20:40] = 1.0  # 사각형
        original_image[20:40, 60:80] = 0.5  # 회색 사각형
    
    print(f"이미지 크기: {original_image.shape}")
    
    # 노이즈 추가
    noisy_image = add_gaussian_noise(original_image, args.noise)
    print(f"노이즈 추가 완료 (분산: {args.noise})")
    
    # 디노이징 적용
    print("Total Variation 처리 중...")
    tv_result = total_variation_denoise(noisy_image)
    
    print("Bilateral Filter 처리 중...")
    bilateral_result = bilateral_denoise(noisy_image)
    
    # 성능 지표 계산
    tv_psnr = calculate_psnr(original_image, tv_result)
    tv_ssim = calculate_ssim(original_image, tv_result)
    bil_psnr = calculate_psnr(original_image, bilateral_result)
    bil_ssim = calculate_ssim(original_image, bilateral_result)
    
    print("\n=== 성능 분석 결과 ===")
    print(f"Total Variation - PSNR: {tv_psnr:.2f}dB, SSIM: {tv_ssim:.3f}")
    print(f"Bilateral Filter - PSNR: {bil_psnr:.2f}dB, SSIM: {bil_ssim:.3f}")
    
    # 결과 시각화
    result_path = os.path.join(args.output, 'comparison_results.png')
    show_comparison_results(original_image, noisy_image, tv_result, bilateral_result, result_path)
    
    # 수렴 분석
    if args.convergence:
        conv_path = os.path.join(args.output, 'convergence_analysis.png')
        print("\n수렴 분석 실행 중...")
        energies, psnr_vals = analyze_convergence(original_image, noisy_image, save_path=conv_path)
        print(f"최종 에너지: {energies[-1]:.2e}")
        print(f"PSNR 개선: {psnr_vals[0]:.2f}dB → {psnr_vals[-1]:.2f}dB")


if __name__ == '__main__':
    main()