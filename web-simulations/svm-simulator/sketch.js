// SVM 데이터와 상태 변수들
let points = [];
let w = null;
let b = 0;
let showSVM = false;
let currentClass = 'A';

function setup() {
    let canvas = createCanvas(400, 400);
    canvas.parent('canvas-container');
    setupButtons();
}

function draw() {
    background(240);
    drawPoints();
    if (showSVM && points.length > 0) {
        drawSVM();
    }
}

function mousePressed() {
    if (mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < height) {
        addPoint(mouseX, mouseY);
    }
}

// 버튼 설정
function setupButtons() {
    select('#resetButton').mousePressed(resetPoints);
    select('#toggleSVMButton').mousePressed(toggleSVM);
    select('#classAButton').mousePressed(() => setClass('A'));
    select('#classBButton').mousePressed(() => setClass('B'));
    select('#saveImageButton').mousePressed(saveVisualization);
}

// 포인트 추가
function addPoint(x, y) {
    points.push({x: x, y: y, label: currentClass});
    if (showSVM) {
        calculateSVM();
    }
}

// 포인트 초기화
function resetPoints() {
    points = [];
    showSVM = false;
}

// SVM 토글
function toggleSVM() {
    showSVM = !showSVM;
    if (showSVM) {
        calculateSVM();
    }
}

// 클래스 설정
function setClass(c) {
    currentClass = c;
}

// 결과 저장
function saveVisualization() {
    let timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    saveCanvas(`svm_result_${timestamp}`, 'png');
}