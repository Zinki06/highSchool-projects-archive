import numpy as np
import matplotlib.pyplot as plt
from skimage import data, img_as_float
from skimage.restoration import denoise_tv_chambolle
from skimage.util import random_noise
from skimage import io
from skimage.util import img_as_float

# 이미지 로드
image_path = "TEST/Image denoising/IMG_1938.JPG"
image = img_as_float(io.imread(image_path))

# 잡음 추가
noisy_image = random_noise(image, mode='gaussian', var=0.01)

# 이미지 복원 (변분법 적용)
restored_image = denoise_tv_chambolle(noisy_image, weight=0.1)

# 시각 자료 준비
fig, axes = plt.subplots(1, 3, figsize=(15, 5),
                         sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(noisy_image)
ax[0].set_title('Noisy Image')

ax[1].imshow(restored_image)
ax[1].set_title('Restored Image')

ax[2].imshow(image)
ax[2].set_title('Original Image')

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()

# 에너지 함수 시각화
def energy_function(u, f, lambda_val=0.1):
    data_term = np.sum((u - f)**2)
    grad_u = np.gradient(u)
    regularization_term = np.sum(np.sqrt(grad_u[0]**2 + grad_u[1]**2))
    return data_term + lambda_val * regularization_term

# 에너지 함수 값 계산
initial_energy = energy_function(noisy_image, image)
final_energy = energy_function(restored_image, image)

print(f"Initial Energy: {initial_energy}")
print(f"Final Energy: {final_energy}")

# 에너지 함수 시각화
iterations = np.arange(1, 11)
energies = [initial_energy]
current_image = noisy_image

for i in iterations[1:]:
    current_image = denoise_tv_chambolle(current_image, weight=0.1)
    energies.append(energy_function(current_image, image))

plt.figure(figsize=(10, 6))
plt.plot(iterations, energies, marker='o')
plt.title('Energy Function over Iterations')
plt.xlabel('Iterations')
plt.ylabel('Energy')
plt.grid(True)
plt.show()
