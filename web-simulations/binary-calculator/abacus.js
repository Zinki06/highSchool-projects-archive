// 주판 관련 전역 상태
const abacusStates = new Map();

// 이진 주판 생성
export function createBinaryAbacus(containerId, bits) {
    const container = document.getElementById(containerId);
    abacusStates.set(containerId, { container, bits });
    
    container.innerHTML = '';
    for (let i = 0; i < bits; i++) {
        const rod = document.createElement('div');
        rod.className = 'rod';
        const bead = document.createElement('div');
        bead.className = 'bead zero';
        bead.onclick = () => toggleBead(containerId, i);
        rod.appendChild(bead);
        container.appendChild(rod);
    }
}

// 구슬 토글
export function toggleBead(containerId, rod) {
    const abacusState = abacusStates.get(containerId);
    if (!abacusState) return;
    
    const bead = abacusState.container.children[rod].getElementsByClassName('bead')[0];
    bead.classList.toggle('zero');
    bead.classList.toggle('one');
    bead.classList.toggle('active');
}

// 숫자 설정
export function setBinaryNumber(containerId, binary) {
    const abacusState = abacusStates.get(containerId);
    if (!abacusState) return;
    
    const bits = binary.padStart(abacusState.bits, '0').split('').reverse();
    for (let i = 0; i < abacusState.bits; i++) {
        const bead = abacusState.container.children[i].getElementsByClassName('bead')[0];
        if (bits[i] === '1') {
            bead.className = 'bead one active';
        } else {
            bead.className = 'bead zero';
        }
    }
}

// 숫자 읽기
export function getBinaryNumber(containerId) {
    const abacusState = abacusStates.get(containerId);
    if (!abacusState) return '';
    
    let binary = '';
    for (let i = abacusState.bits - 1; i >= 0; i--) {
        const bead = abacusState.container.children[i].getElementsByClassName('bead')[0];
        binary += bead.classList.contains('active') ? '1' : '0';
    }
    return binary;
}