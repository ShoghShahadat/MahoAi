// ارسال فرم و دریافت پاسخ
document.getElementById('dataForm').addEventListener('submit', async function(event) {
  event.preventDefault();
  const text = document.getElementById('textInput').value;
  const outputDiv = document.getElementById('output');

  outputDiv.innerHTML = '<p style="color: #b0b0b0;">در حال پردازش...</p>';

  try {
    const response = await fetch('http://127.0.0.1:8283/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();

    outputDiv.innerHTML = formatJsonToItems(data);
    document.getElementById('applyChangesBtn').style.display = 'block';
    attachApplyChangesListener();
  } catch (error) {
    console.error('Error:', error);
    outputDiv.innerHTML = `<p style="color: #ff6f61;">خطا در ارسال داده‌ها: ${error.message}</p>`;
  }
});

// تابع برای تبدیل JSON به آیتم‌ها
function formatJsonToItems(data) {
  let html = '';

  if (data.message) {
    html += `
      <div class="item">
        <div class="item-title">پیام:</div>
        <div class="item-content">${data.message}</div>
      </div>`;
  }

  if (data.pip && data.pip.trim() !== '') {
    html += `
      <div class="item">
        <div class="item-title">کتاب‌خونه‌ها:</div>
        <div class="item-content">${data.pip}</div>
        <button id="install-lib-button" style="display:block; margin-top: 10px;">نصب کتابخانه‌ها</button>
      </div>`;
  }

  if (data.log) {
    html += `
      <div class="item">
        <div class="item-title">گزارش:</div>
        <div class="item-content">${data.log}</div>
      </div>`;
  }

  if (data.edits && Array.isArray(data.edits)) {
    data.edits.forEach((edit, index) => {
      html += `
        <div class="item">
          <div class="item-title2" style="color: #ff8a80;">ویرایش ${index + 1}:</div>
          <div class="item-content">
            <div class="nested-item"><strong style="color: #70dbdb;">مسیر:</strong> ${edit.path || 'نامشخص'}</div>
            <div class="nested-item"><strong style="color: #70dbdb;">گزارش:</strong> ${edit.log || 'بدون گزارش'}</div>
            <div class="nested-item"><strong style="color: #70dbdb;">توضیحات:</strong> ${edit.info || 'بدون توضیحات'}</div>
            ${edit.edits && Array.isArray(edit.edits) ? edit.edits.map((subEdit, subIndex) => `
              <div class="nested-item">
                <strong style="color: #ff8a80;">ویرایش ${subIndex + 1}:</strong><br>
                <strong style="color: #a5d6a7;">خطوط:</strong> ${subEdit.start_number_line || '؟'} <strong style="color: #a5d6a7;">تا</strong> ${subEdit.end_number_line || '؟'}<br>
                <strong style="color: #a5d6a7;">نوع:</strong> ${subEdit.type || 'نامشخص'}<br>
                کد جدید: <pre>${subEdit.new_code || 'بدون کد'}</pre>
              </div>`).join('') : ''}
          </div>
        </div>`;
    });
  }

  // انتقال نصب دکمه به خارج از setTimeout
  setTimeout(() => {
    attachInstallButtonListener();
  }, 0);

  return html;
}

function attachInstallButtonListener() {
  const installButton = document.getElementById('install-lib-button');
  if (installButton) {
    installButton.addEventListener('click', async () => {
      try {
        const response = await fetch('http://127.0.0.1:8283/pip');
        const data = await response.json();
        alert(data.status === 'success' ? 'کتابخانه‌ها با موفقیت نصب شدند.' : `خطا در نصب کتابخانه‌ها: ${data.error || 'نامشخص'}`);
      } catch (error) {
        console.error('Error:', error);
        alert('مشکلی در برقراری ارتباط با سرور پیش آمده.');
      }
    });
  }
}

// اتصال رویداد به دکمه اعمال تغییرات
function attachApplyChangesListener() {
  const applyChangesBtn = document.getElementById('applyChangesBtn');
  if (applyChangesBtn) {
    applyChangesBtn.removeEventListener('click', handleApplyChanges); // حذف رویداد قبلی
    applyChangesBtn.addEventListener('click', handleApplyChanges);
  }
}

async function handleApplyChanges() {
  try {
    const response = await fetch('http://127.0.0.1:8283/set_json', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(getEditsFromPage())
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();

    alert('تغییرات با موفقیت اعمال شد.');
    await populateBackupVersions();
    console.log('پاسخ از سرور:', data);
  } catch (error) {
    console.error('خطا در ارسال درخواست:', error);
    alert(`خطا در ارسال درخواست اعمال تغییرات: ${error.message}`);
  }
}

function getEditsFromPage() {
  return { message: 'تغییرات اعمال شد.' }; // منطق جمع‌آوری داده‌ها باید اینجا پیاده‌سازی بشه
}

async function populateBackupVersions() {
  try {
    const response = await fetch('http://127.0.0.1:8283/list_versions');
    const data = await response.json();
    const versionDropdown = document.getElementById('backupVersion');
    if (versionDropdown) {
      versionDropdown.innerHTML = data.versions.map(version =>
        `<option value="${version}">Version ${version}</option>`
      ).join('');
    }
  } catch (error) {
    console.error('Error fetching backup versions:', error);
  }
}

function showRestoreDialog() {
  const version = document.getElementById('backupVersion').value;
  if (confirm(`آیا مطمئن هستید که می‌خواهید نسخه ${version} را بازیابی کنید؟`)) {
    restoreBackup(version);
  }
}

async function restoreBackup(version) {
  try {
    const response = await fetch(`http://127.0.0.1:8283/restore_version/${version}`, { method: 'POST' });
    const data = await response.json();
    alert(data.message || 'نسخه با موفقیت بازیابی شد.');
  } catch (error) {
    console.error('Error restoring version:', error);
    alert('خطا در بازیابی نسخه.');
  }
}

function createBackupRestoreElements() {
  const formContainer = document.querySelector('.form-container') || document.body;

  formContainer.insertAdjacentHTML('beforeend', `
    <label for="backupVersion">انتخاب نسخه بکاپ:</label>
    <select id="backupVersion" name="backupVersion"></select>
    <button type="button" id="restoreBackupBtn" style="background-color: #dc3545; border-color: #dc3545; color: white;">بازیابی بکاپ</button>
  `);

  document.getElementById('restoreBackupBtn').addEventListener('click', showRestoreDialog);
  populateBackupVersions();
}

// حذف خطای await در سطح بالا
(function() {
  createBackupRestoreElements();
})();

async function requestNewPathFromServer() {
  try {
    const response = await fetch('http://127.0.0.1:8283/set_path');
    const data = await response.json();
    if (data.status === 'success' && data.path) {
      displaySelectedPath(data.path);
      console.log('✅ مسیر جدید:', data.path);
      await populateBackupVersions();
    } else {
      console.error('❌ خطا در دریافت مسیر:', data.error || data.message);
    }
  } catch (error) {
    console.error('⚠️ خطا:', error);
  }
}

function displaySelectedPath(path) {
  let displayDiv = document.getElementById('selectedPathDisplay');
  if (!displayDiv) {
    displayDiv = document.createElement('div');
    displayDiv.id = 'selectedPathDisplay';
    document.body.appendChild(displayDiv);
  }
  displayDiv.innerHTML = `📂 <strong>مسیر انتخاب شده:</strong> ${path}`;
  displayDiv.style.cursor = 'pointer';
  displayDiv.onclick = requestNewPathFromServer;
}

async function checkAndSelectPath() {
  try {
    const response = await fetch('http://127.0.0.1:8283/path');
    const data = await response.json();
    if (data.path) {
      displaySelectedPath(data.path);
    } else {
      await requestNewPathFromServer();
    }
  } catch (error) {
    console.error('⚠️ خطا در دریافت مسیر:', error);
  }
}

// اجرای تابع به صورت غیرهمزمان
(async () => {
  await checkAndSelectPath();
})();

// افزودن ستاره‌ها
const colors = ['#6d1e78', '#155950', '#9370db', '#ffffff', '#add8e6'];
for (let i = 0; i < 200; i++) {
  const star = document.createElement('div');
  star.classList.add('star');
  Object.assign(star.style, {
    left: `${Math.random() * 100}vw`,
    top: `${Math.random() * 100}vh`,
    animationDelay: `${Math.random() * 2}s`,
    backgroundColor: colors[Math.floor(Math.random() * colors.length)]
  });
  document.body.appendChild(star);
}