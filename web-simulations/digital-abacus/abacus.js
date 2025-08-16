// 주판 컨테이너 전역 상태
let abacusContainer;

// 전통 주판 생성
export function createAbacus(containerId) {
    abacusContainer = document.getElementById(containerId);
    
    abacusContainer.innerHTML = '';
    for (let i = 0; i < 7; i++) {
        const rod = document.createElement('div');
        rod.className = 'rod';
        const separator = document.createElement('div');
        separator.className = 'separator';
        rod.appendChild(separator);
        const fiveBead = document.createElement('div');
        fiveBead.className = 'bead five';
        fiveBead.onclick = () => toggleBead(i, 'five');
        rod.appendChild(fiveBead);
        for (let j = 0; j < 4; j++) {
            const oneBead = document.createElement('div');
            oneBead.className = 'bead one';
            oneBead.onclick = () => toggleBead(i, 'one', j);
            rod.appendChild(oneBead);
        }
        abacusContainer.appendChild(rod);
    }
}

// 구슬 토글
export function toggleBead(rod, type, index) {
    if (!abacusContainer) return;
    
    const beads = abacusContainer.children[rod].getElementsByClassName(`bead ${type}`);
    if (type === 'five') {
        beads[0].classList.toggle('active');
    } else {
        for (let i = 0; i <= index; i++) {
            beads[i].classList.add('active');
        }
        for (let i = index + 1; i < beads.length; i++) {
            beads[i].classList.remove('active');
        }
    }
}

// 숫자 설정
export function setAbacusNumber(number) {
    if (!abacusContainer) return;
    
    let abacusNumber = number < 0 ? 10000000 + number : number;
    const digits = abacusNumber.toString().padStart(7, '0').split('').reverse();
    for (let i = 0; i < 7; i++) {
        const rod = abacusContainer.children[i];
        const fiveBead = rod.getElementsByClassName('bead five')[0];
        const oneBeads = rod.getElementsByClassName('bead one');
        const digit = parseInt(digits[i]);
        fiveBead.classList.toggle('active', digit >= 5);
        for (let j = 0; j < 4; j++) {
            oneBeads[j].classList.toggle('active', j < (digit % 5));
        }
    }
}

// 주판 초기화
export function clearAbacus() {
    if (!abacusContainer) return;
    
    const beads = abacusContainer.getElementsByClassName('bead');
    for (let bead of beads) {
        bead.classList.remove('active');
    }
}

// 주판 값 읽기
export function getAbacusValue() {
    if (!abacusContainer) return 0;
    
    let result = 0;
    for (let i = 0; i < 7; i++) {
        const rod = abacusContainer.children[i];
        const fiveBead = rod.getElementsByClassName('bead five')[0];
        const oneBeads = rod.getElementsByClassName('bead one');
        let rodValue = fiveBead.classList.contains('active') ? 5 : 0;
        for (let oneBead of oneBeads) {
            if (oneBead.classList.contains('active')) rodValue++;
        }
        result += rodValue * Math.pow(10, i);
    }
    
    // 음수 처리
    if (result >= 5000000) {
        result = result - 10000000;
    }
    
    return result;
}