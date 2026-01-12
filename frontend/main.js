// 元素绑定
const fileInput = document.getElementById('fileInput');
const selectFileBtn = document.getElementById('selectFileBtn');
const fileNameDisplay = document.getElementById('fileNameDisplay');
const uploadBtn = document.getElementById('uploadBtn');
const resultArea = document.getElementById('resultArea');
const resultSummary = document.getElementById('resultSummary');
const errorList = document.getElementById('errorList');

// 选择文件
selectFileBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileNameDisplay.textContent = file.name;
    } else {
        fileNameDisplay.textContent = '未选择文件';
    }
});

// 上传+检测逻辑
uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        alert('请先选择CSV文件！');
        return;
    }

    // 1. 上传文件
    const formData = new FormData();
    formData.append('file', file);

    try {
        // 上传请求
        const uploadRes = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });
        const uploadData = await uploadRes.json();

        if (uploadData.status !== 'success') {
            alert(`上传失败：${uploadData.message}`);
            return;
        }

        // 2. 上传成功后，调用检测接口
        const detectRes = await fetch('http://localhost:5000/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: uploadData.filename  // 传后端返回的唯一文件名
            })
        });
        const detectData = await detectRes.json();

        // 3. 渲染检测结果
        renderResult(detectData);

    } catch (err) {
        alert(`操作失败：${err.message}`);
    }
});

// 渲染检测结果
function renderResult(data) {
    resultArea.style.display = 'block';
    if (data.status !== 'success') {
        resultSummary.textContent = `检测失败：${data.message}`;
        errorList.innerHTML = '';
        return;
    }

    // 渲染摘要
    resultSummary.textContent = data.summary;

    // 渲染错误详情
    if (data.error_count > 0) {
        let errorHtml = '';
        data.error_details.forEach((error, index) => {
            errorHtml += `<p>${index + 1}. ${error}</p>`;
        });
        errorList.innerHTML = errorHtml;
    } else {
        errorList.innerHTML = '<p style="color: #28a745;">未发现合规问题</p>';
    }
}
