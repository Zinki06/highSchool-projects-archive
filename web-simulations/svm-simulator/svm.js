// SVM 계산 함수
function calculateSVM() {
    if (points.length < 2) return;

    w = createVector(random(-1, 1), random(-1, 1));
    b = random(-1, 1);
    
    for (let i = 0; i < 1000; i++) {
        let error = false;
        for (let p of points) {
            let x = createVector(p.x / width - 0.5, p.y / height - 0.5);
            let y = p.label === 'A' ? 1 : -1;
            let activation = w.dot(x) + b;
            if (y * activation <= 0) {
                w.add(p5.Vector.mult(x, y * 0.1));
                b += y * 0.1;
                error = true;
            }
        }
        if (!error) break;
    }
}

// 포인트 그리기
function drawPoints() {
    for (let p of points) {
        fill(p.label === 'A' ? color(231, 76, 60) : color(52, 152, 219));
        ellipse(p.x, p.y, 10, 10);
    }
}

// SVM 경계선 그리기
function drawSVM() {
    drawLine(0, 'black', 2);
    drawLine(1, 'red', 1);
    drawLine(-1, 'red', 1);
}

// 경계선 그리기 헬퍼 함수
function drawLine(offset, strokeColor, weight) {
    let b2 = b + offset;
    strokeWeight(weight);
    if (abs(w.y) > abs(w.x)) {
        let x1 = (-b2 - w.x * -0.5) / w.y * height + height / 2;
        let x2 = (-b2 - w.x * 0.5) / w.y * height + height / 2;
        stroke(strokeColor);
        line(0, x1, width, x2);
    } else {
        let y1 = (-b2 - w.y * -0.5) / w.x * width + width / 2;
        let y2 = (-b2 - w.y * 0.5) / w.x * width + width / 2;
        stroke(strokeColor);
        line(y1, 0, y2, height);
    }
}