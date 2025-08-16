export function addBinary(a, b, bits) {
    let carry = 0;
    let result = '';
    let steps = [];

    for (let i = bits - 1; i >= 0; i--) {
        const sum = parseInt(a[i]) + parseInt(b[i]) + carry;
        result = (sum % 2) + result;
        carry = Math.floor(sum / 2);
        steps.push(`위치 ${bits - i}: ${a[i]} + ${b[i]} + ${carry} (올림) = ${sum}, 결과 비트: ${sum % 2}, 새로운 올림: ${Math.floor(sum / 2)}`);
    }

    return { result, steps };
}

export function subtractBinary(a, b, bits) {
    let borrow = 0;
    let result = '';
    let steps = [];

    for (let i = bits - 1; i >= 0; i--) {
        let diff = parseInt(a[i]) - parseInt(b[i]) - borrow;
        if (diff < 0) {
            diff += 2;
            borrow = 1;
        } else {
            borrow = 0;
        }
        result = diff + result;
        steps.push(`위치 ${bits - i}: ${a[i]} - ${b[i]} - ${borrow} (빌림) = ${diff}, 결과 비트: ${diff}, 새로운 빌림: ${borrow}`);
    }

    return { result, steps };
}

export function multiplyBinary(a, b, bits) {
    let result = '0'.repeat(bits);
    let steps = [];

    for (let i = bits - 1; i >= 0; i--) {
        if (b[i] === '1') {
            let shiftedA = a + '0'.repeat(bits - 1 - i);
            let addResult = addBinary(result, shiftedA.slice(-bits), bits);
            result = addResult.result;
            steps.push(`${bits - i}번째 비트가 1이므로 ${a}를 ${bits - 1 - i}만큼 왼쪽 시프트하여 더함`);
            steps = steps.concat(addResult.steps);
        } else {
            steps.push(`${bits - i}번째 비트가 0이므로 아무 작업도 하지 않음`);
        }
    }

    return { result, steps };
}

export function divideBinary(a, b, bits) {
    if (b === '0'.repeat(bits)) {
        return { result: '오류: 0으로 나눌 수 없습니다', steps: ['0으로 나누려고 시도함'] };
    }

    let quotient = '0'.repeat(bits);
    let remainder = a;
    let steps = [];

    for (let i = 0; i < bits; i++) {
        let shiftedRemainder = remainder.slice(1) + '0';
        let subtractResult = subtractBinary(shiftedRemainder, b, bits);
        
        if (subtractResult.result[0] !== '1') {  // If the result is non-negative
            remainder = subtractResult.result;
            quotient = quotient.slice(1) + '1';
            steps.push(`단계 ${i + 1}: 나머지를 왼쪽으로 시프트하고 ${b}를 뺌. 결과가 음수가 아니므로 몫에 1을 추가`);
        } else {
            remainder = shiftedRemainder;
            quotient = quotient.slice(1) + '0';
            steps.push(`단계 ${i + 1}: 나머지를 왼쪽으로 시프트함. ${b}를 뺄 수 없으므로 몫에 0을 추가`);
        }
        steps = steps.concat(subtractResult.steps);
    }

    return { result: quotient, remainder, steps };
}