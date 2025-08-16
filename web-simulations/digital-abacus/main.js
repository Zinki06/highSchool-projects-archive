import { createAbacus, setAbacusNumber, clearAbacus, getAbacusValue } from './abacus.js';

// 초기화
function init() {
    createAbacus('abacus');
    setupEventListeners();
    updateResult();
}

// 이벤트 리스너 설정
function setupEventListeners() {
    document.getElementById('setNumber').addEventListener('click', setNumber);
    document.getElementById('clearAbacus').addEventListener('click', clearAbacusHandler);
    document.getElementById('saveAbacus').addEventListener('click', saveAbacusState);
    document.getElementById('abacus').addEventListener('click', updateResult);
}

// 숫자 설정
function setNumber() {
    const input = document.getElementById('input').value;
    const number = parseInt(input);
    if (isNaN(number) || Math.abs(number) > 9999999) {
        alert('유효한 숫자를 입력해주세요 (-9999999 ~ 9999999).');
        return;
    }
    
    setAbacusNumber(number);
    updateResult();
}

// 주판 초기화
function clearAbacusHandler() {
    clearAbacus();
    document.getElementById('input').value = '';
    updateResult();
}

// 결과 업데이트
function updateResult() {
    const result = getAbacusValue();
    document.getElementById('result').textContent = `현재 값: ${result}`;
}

// 주판 상태 저장
function saveAbacusState() {
    const currentValue = getAbacusValue();
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    
    // 주판 상태 분석
    const abacusState = getAbacusStateInfo();
    
    const content = `전통 주판 상태 저장 - ${timestamp}\n\n` +
                   `현재 표시 숫자: ${currentValue}\n\n` +
                   `각 자릿수별 구슬 상태:\n${abacusState}\n\n` +
                   `주판 읽는 법:\n` +
                   `- 5주판 활성(●): 5의 가치\n` +
                   `- 1주판 활성(●): 1의 가치\n` +
                   `- 비활성(○): 0의 가치`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `abacus_state_${timestamp}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// 주판 상태 분석
function getAbacusStateInfo() {
    let state = '';
    const digitNames = ['일의 자리', '십의 자리', '백의 자리', '천의 자리', '만의 자리', '십만의 자리', '백만의 자리'];
    const container = document.getElementById('abacus');
    
    for (let i = 0; i < 7; i++) {
        const rod = container.children[i];
        const fiveBead = rod.getElementsByClassName('bead five')[0];
        const oneBeads = rod.getElementsByClassName('bead one');
        
        const fiveActive = fiveBead.classList.contains('active');
        let oneCount = 0;
        for (let oneBead of oneBeads) {
            if (oneBead.classList.contains('active')) oneCount++;
        }
        
        const digitValue = (fiveActive ? 5 : 0) + oneCount;
        state += `${digitNames[i]}: ${digitValue} (5주판: ${fiveActive ? '●' : '○'}, 1주판: ${oneCount}개)\n`;
    }
    
    return state;
}

// 초기화 실행
init();