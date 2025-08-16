import { createBinaryAbacus, setBinaryNumber, getBinaryNumber } from './abacus.js';
import { addBinary, subtractBinary, multiplyBinary, divideBinary } from './binaryOperations.js';

const BITS = 16;

// 초기화
function init() {
    createBinaryAbacus('abacusA', BITS);
    createBinaryAbacus('abacusB', BITS);
    createBinaryAbacus('abacusResult', BITS);
    setupEventListeners();
    calculateRealtime();
}

// 이벤트 리스너 설정
function setupEventListeners() {
    document.getElementById('inputA').addEventListener('input', () => handleInput('A'));
    document.getElementById('inputB').addEventListener('input', () => handleInput('B'));
    document.getElementById('operation').addEventListener('change', calculateRealtime);
    document.getElementById('saveResult').addEventListener('click', saveResult);
    document.getElementById('abacusA').addEventListener('click', () => handleAbacusClick('A'));
    document.getElementById('abacusB').addEventListener('click', () => handleAbacusClick('B'));
}

// 입력 처리
function handleInput(abacus) {
    const input = document.getElementById(`input${abacus}`);
    input.value = input.value.replace(/[^01]/g, '').substring(0, BITS);
    
    setBinaryNumber(`abacus${abacus}`, input.value);
    calculateRealtime();
}

// 주판 클릭 처리
function handleAbacusClick(abacus) {
    const binary = getBinaryNumber(`abacus${abacus}`);
    document.getElementById(`input${abacus}`).value = binary;
    calculateRealtime();
}

// 실시간 계산
function calculateRealtime() {
    const binaryA = getBinaryNumber('abacusA').padStart(BITS, '0');
    const binaryB = getBinaryNumber('abacusB').padStart(BITS, '0');
    const operation = document.getElementById('operation').value;

    let result, steps, remainder;

    switch (operation) {
        case 'add':
            ({ result, steps } = addBinary(binaryA, binaryB, BITS));
            break;
        case 'subtract':
            ({ result, steps } = subtractBinary(binaryA, binaryB, BITS));
            break;
        case 'multiply':
            ({ result, steps } = multiplyBinary(binaryA, binaryB, BITS));
            break;
        case 'divide':
            ({ result, remainder, steps } = divideBinary(binaryA, binaryB, BITS));
            break;
    }

    setBinaryNumber('abacusResult', result);

    const decimalA = parseInt(binaryA, 2);
    const decimalB = parseInt(binaryB, 2);
    const decimalResult = parseInt(result, 2);

    let resultText = `계산: ${binaryA} ${getOperationSymbol(operation)} ${binaryB}<br>
                      결과 (이진수): ${result}<br>
                      결과 (십진수): ${decimalResult}`;

    if (operation === 'divide' && remainder) {
        resultText += `<br>나머지 (이진수): ${remainder}<br>
                       나머지 (십진수): ${parseInt(remainder, 2)}`;
    }

    document.getElementById('result').innerHTML = resultText;
    document.getElementById('steps').innerHTML = steps.join('<br>');
}

// 연산 기호 반환
function getOperationSymbol(operation) {
    switch (operation) {
        case 'add': return '+';
        case 'subtract': return '-';
        case 'multiply': return '×';
        case 'divide': return '÷';
        default: return '';
    }
}

// 결과 저장
function saveResult() {
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const resultContent = document.getElementById('result').innerHTML;
    const stepsContent = document.getElementById('steps').innerHTML;
    
    const fullContent = `이진수 계산 결과 - ${timestamp}\n\n` +
                       `${resultContent.replace(/<br>/g, '\n')}\n\n` +
                       `계산 과정:\n${stepsContent.replace(/<br>/g, '\n')}`;
    
    const blob = new Blob([fullContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `binary_calculation_${timestamp}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// 초기화 실행
init();