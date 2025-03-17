document.getElementById('dataForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const text = document.getElementById('textInput').value;
  const outputDiv = document.getElementById('output');

  outputDiv.innerHTML = '<p style="color: #b0b0b0;">در حال پردازش...</p>';

  fetch('http://127.0.0.1:8283/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: text })
  })
  .then(response => response.json())
  .then(data => {
    outputDiv.innerHTML = formatJsonToItems(data);
    document.getElementById('applyChangesBtn').style.display = 'block';
  })
  .catch(error => {
    console.error('Error:', error);
    outputDiv.innerHTML = `<p style="color: #ff6f61;">خطا در ارسال داده‌ها: ${error.message}</p>`;
  });
});

// تابع برای تبدیل JSON به HTML
function formatJsonToItems(data) {
  let html = '';

  if (data.message) {
    html += `<div class="item"><div class="item-title">پیام:</div><div class="item-content">${data.message}</div></div>`;
  }

  if ('pip' in data) {
    html += `<div class="item"><div class="item-title">کتاب‌خونه‌ها:</div>
             <div class="item-content">${data.pip || 'هیچ کتابخانه‌ای مشخص نشده'}</div>
             <button id="install-lib-button" style="display:block; margin-top: 10px;">نصب کتابخانه‌ها</button></div>`;
  }

  if (data.log) {
    html += `<div class="item"><div class="item-title">گزارش:</div><div class="item-content">${data.log}</div></div>`;
  }

  if (data.edits && Array.isArray(data.edits)) {
    data.edits.forEach((edit, index) => {
      html += `<div class="item">
                 <div class="item-title2">ویرایش ${index + 1}:</div>
                 <div class="item-content">
                   <div class="nested-item"><strong>مسیر:</strong> ${edit.path}</div>
                   <div class="nested-item"><strong>گزارش:</strong> ${edit.log}</div>`;
      if (edit.edits && Array.isArray(edit.edits)) {
        edit.edits.forEach((subEdit, subIndex) => {
          html += `<div class="nested-item">
                     <strong>ویرایش ${subIndex + 1}:</strong><br>
                     خطوط: ${subEdit.start_number_line} تا ${subEdit.end_number_line}<br>
                     نوع: ${subEdit.type}<br>
                     کد جدید: <pre>${subEdit.new_code}</pre>
                   </div>`;
        });
      }
      html += `</div></div>`;
    });
  }

  setTimeout(() => attachEventListeners(), 0);
  return html;
}

// تابع اتصال رویدادها بعد از بارگیری HTML
function attachEventListeners() {
  const installButton = document.getElementById('install-lib-button');
  if (installButton) {
    installButton.addEventListener('click', function() {
      fetch('http://127.0.0.1:8283/pip', { method: 'GET' })
      .then(response => response.json())
      .then(data => {
        alert(data.status === 'success' ? 'کتابخانه‌ها با موفقیت نصب شدند.' : `خطا در نصب کتابخانه‌ها: ${data.error || 'نامشخص'}`);
      })
      .catch(error => alert('مشکلی در برقراری ارتباط با سرور پیش آمده.'));
    });
  }

  const applyChangesBtn = document.getElementById('applyChangesBtn');
  if (applyChangesBtn) {
    applyChangesBtn.addEventListener('click', function() {
      fetch('http://127.0.0.1:8283/set_json', { method: 'GET' })
      .then(response => response.json())
      .then(data => {
        alert('درخواست اعمال تغییرات با موفقیت ارسال شد.');
        applyChangesBtn.style.backgroundColor = 'green';
      })
      .catch(error => {
        alert('خطا در ارسال درخواست اعمال تغییرات.');
        applyChangesBtn.style.backgroundColor = 'red';
      });
    });
  }
}

// دریافت مسیر از سرور
function checkAndSelectPath() {
  fetch('http://127.0.0.1:8283/path', { method: 'GET' })
  .then(response => response.json())
  .then(data => {
    if (data.path) {
      displaySelectedPath(data.path);
    } else {
      requestNewPathFromServer();
    }
  })
  .catch(error => console.error('⚠️ خطا در دریافت مسیر:', error));
}

// درخواست مسیر جدید
function requestNewPathFromServer() {
  fetch('http://127.0.0.1:8283/set_path', { method: 'GET' })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      displaySelectedPath(data.path);
    } else {
      console.error('❌ خطا در دریافت مسیر:', data.error || data.message);
    }
  })
  .catch(error => console.error('⚠️ خطا:', error));
}

// نمایش مسیر انتخاب‌شده
function displaySelectedPath(path) {
  const displayDiv = document.getElementById('selectedPathDisplay');
  displayDiv.innerHTML = `📂 <strong>مسیر انتخاب شده:</strong> ${path}`;
  displayDiv.style.cursor = 'pointer';
  displayDiv.onclick = requestNewPathFromServer;  // جلوگیری از افزودن چندین Event Listener
}

// ایجاد ستاره‌ها در پس‌زمینه
function createStars() {
  const colors = ['#6d1e78', '#155950', '#9370db', '#ffffff', '#add8e6'];
  for (let i = 0; i < 200; i++) {
    const star = document.createElement('div');
    star.classList.add('star');
    star.style.left = `${Math.random() * 100}vw`;
    star.style.top = `${Math.random() * 100}vh`;
    star.style.animationDelay = `${Math.random() * 2}s`;
    star.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    document.body.appendChild(star);
  }
}

checkAndSelectPath();

// تابع برای لیست کردن بکاپ‌ها
function listBackups(filePath) {
    fetch(`/list_backups?file_path=${encodeURIComponent(filePath)}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            if (data.backups && data.backups.length > 0) {
                displayBackups(data.backups, filePath);
            } else {
                alert('هیچ بکاپی برای این فایل وجود ندارد.');
            }
        })
        .catch(error => console.error('Error:', error));
}

// تابع نمایش بکاپ ها و ایجاد دکمه بازگردانی
function displayBackups(backups, filePath) {
    const outputDiv = document.getElementById('output');
    let backupsHTML = '<h4>بکاپ‌های موجود:</h4><ul>';
    backups.forEach(backup => {
        backupsHTML += `<li>${backup} <button onclick=\"restoreBackup('${backup}', '${filePath}')\">بازگردانی</button></li>`;
    });
    backupsHTML += '</ul>';
    outputDiv.innerHTML += backupsHTML;
}

// تابع بازگردانی بکاپ
function restoreBackup(backupPath, filePath) {
    fetch('/restore_backup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                backup_path: backupPath,
                file_path: filePath
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
        })
        .catch(error => console.error('Error:', error));
}

// اضافه کردن دکمه لیست بکاپ به هر آیتم فایل
function formatJsonToItems(data) {
 let html = '';

    if (data.message) {
        html += `<div class=\"item\"><div class=\"item-title\">پیام:</div><div class=\"item-content\">${data.message}</div></div>`;
    }

    if ('pip' in data) {
        html += `<div class=\"item\"><div class=\"item-title\">کتاب‌خونه‌ها:</div>
         <div class=\"item-content\">${data.pip || 'هیچ کتابخانه‌ای مشخص نشده'}</div>
         <button id=\"install-lib-button\" style=\"display:block; margin-top: 10px;\">نصب کتابخانه‌ها</button></div>`;
    }

    if (data.log) {
        html += `<div class=\"item\"><div class=\"item-title\">گزارش:</div><div class=\"item-content\">${data.log}</div></div>`;
    }

    if (data.edits && Array.isArray(data.edits)) {
        data.edits.forEach((edit, index) => {
            html += `<div class=\"item\">   <button onclick=\"listBackups('${edit.path}')\">لیست بکاپ ها</button>
             <div class=\"item-title2\">ویرایش ${index + 1}:</div>
             <div class=\"item-content\">
             <div class=\"nested-item\"><strong>مسیر:</strong> ${edit.path}</div>
             <div class=\"nested-item\"><strong>گزارش:</strong> ${edit.log}</div>`;

            if (edit.edits && Array.isArray(edit.edits)) {
                edit.edits.forEach((subEdit, subIndex) => {
                    html += `<div class=\"nested-item\">
                    <strong>ویرایش ${subIndex + 1}:</strong><br>
                     خطوط: ${subEdit.start_number_line} تا ${subEdit.end_number_line}<br>
                    نوع: ${subEdit.type}<br>
                     کد جدید: <pre>${subEdit.new_code}</pre>
                    </div>`;
                });
            }
            html += `</div></div>`;
        });
    }

 setTimeout(() => attachEventListeners(), 0);
 return html;

}


createStars();
