/* ============================================
   LMS TEMPLATE - MAIN JAVASCRIPT
   ============================================ */

'use strict';

// ── Helpers ──────────────────────────────────
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const on = (el, ev, fn, opts) => el && el.addEventListener(ev, fn, opts);

// ── Init on DOM ready ────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initDarkMode();
  initSidebar();
  initScrollTop();
  initPasswordToggle();
  initOTPInputs();
  initCounters();
  initProgressBars();
  initFileUpload();
  initCalendar();
  initToasts();
  initQuiz();
  initChatInput();
  initKanban();
  initSkeletons();
  initAOS();
  initCharts();
});

// ── 1. DARK MODE ─────────────────────────────
function initDarkMode() {
  const saved = localStorage.getItem('lms-theme') || 'light';
  document.documentElement.setAttribute('data-bs-theme', saved);

  $$('[data-dark-toggle]').forEach(toggle => {
    on(toggle, 'click', () => {
      const current = document.documentElement.getAttribute('data-bs-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-bs-theme', next);
      localStorage.setItem('lms-theme', next);
    });
  });
}

// ── 2. SIDEBAR ───────────────────────────────
function initSidebar() {
  const sidebar = $('.sidebar');
  const overlay = $('.sidebar-overlay');
  const openBtn = $('#sidebarToggle');
  const closeBtn = $('#sidebarClose');

  function openSidebar() {
    sidebar?.classList.add('show');
    overlay?.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    sidebar?.classList.remove('show');
    overlay?.classList.remove('show');
    document.body.style.overflow = '';
  }

  on(openBtn, 'click', openSidebar);
  on(closeBtn, 'click', closeSidebar);
  on(overlay, 'click', closeSidebar);

  // Submenu collapse
  $$('.sidebar-link[data-bs-toggle="collapse"]').forEach(link => {
    on(link, 'click', () => {
      const arrow = link.querySelector('.arrow');
      if (arrow) {
        const isExpanded = link.getAttribute('aria-expanded') === 'true';
        arrow.style.transform = isExpanded ? '' : 'rotate(90deg)';
      }
    });
  });
}

// ── 3. SCROLL TO TOP ─────────────────────────
function initScrollTop() {
  const btn = $('.scroll-top');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('show', window.scrollY > 300);
  });
  on(btn, 'click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// ── 4. PASSWORD TOGGLE ───────────────────────
function initPasswordToggle() {
  $$('.password-toggle').forEach(toggle => {
    on(toggle, 'click', () => {
      const input = toggle.closest('.position-relative').querySelector('input');
      if (!input) return;
      const isPass = input.type === 'password';
      input.type = isPass ? 'text' : 'password';
      toggle.innerHTML = isPass ? '<i class="bi bi-eye-slash"></i>' : '<i class="bi bi-eye"></i>';
    });
  });
}

// ── 5. OTP INPUTS ────────────────────────────
function initOTPInputs() {
  const inputs = $$('.otp-input');
  inputs.forEach((input, i) => {
    on(input, 'input', () => {
      if (input.value.length === 1 && inputs[i + 1]) {
        inputs[i + 1].focus();
      }
    });
    on(input, 'keydown', e => {
      if (e.key === 'Backspace' && !input.value && inputs[i - 1]) {
        inputs[i - 1].focus();
      }
    });
    on(input, 'paste', e => {
      e.preventDefault();
      const pasted = (e.clipboardData || window.clipboardData).getData('text').slice(0, inputs.length);
      [...pasted].forEach((ch, j) => {
        if (inputs[i + j]) inputs[i + j].value = ch;
      });
      if (inputs[i + pasted.length - 1]) inputs[i + pasted.length - 1].focus();
    });
  });
}

// ── 6. ANIMATED COUNTERS ─────────────────────
function initCounters() {
  const counters = $$('[data-counter]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseFloat(el.dataset.counter);
        const decimals = el.dataset.decimals ? parseInt(el.dataset.decimals) : 0;
        const suffix = el.dataset.suffix || '';
        const prefix = el.dataset.prefix || '';
        const duration = 1800;
        const start = performance.now();

        function update(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
          const value = eased * target;
          el.textContent = prefix + value.toFixed(decimals) + suffix;
          if (progress < 1) requestAnimationFrame(update);
        }

        requestAnimationFrame(update);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

// ── 7. PROGRESS BARS ─────────────────────────
function initProgressBars() {
  const bars = $$('[data-progress]');
  if (!bars.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        const width = bar.dataset.progress;
        bar.style.width = width + '%';
        observer.unobserve(bar);
      }
    });
  }, { threshold: 0.3 });

  bars.forEach(bar => {
    bar.style.width = '0%';
    bar.style.transition = 'width 1.2s ease';
    observer.observe(bar);
  });
}

// ── 8. FILE UPLOAD DRAG & DROP ───────────────
function initFileUpload() {
  $$('.file-upload-area').forEach(area => {
    const input = area.querySelector('input[type="file"]');

    ['dragover', 'dragenter'].forEach(ev => {
      on(area, ev, e => {
        e.preventDefault();
        area.classList.add('dragover');
      });
    });
    ['dragleave', 'dragend', 'drop'].forEach(ev => {
      on(area, ev, e => {
        e.preventDefault();
        area.classList.remove('dragover');
      });
    });
    on(area, 'drop', e => {
      const files = e.dataTransfer.files;
      handleFiles(files, area);
    });
    on(area, 'click', () => input?.click());
    on(input, 'change', () => handleFiles(input.files, area));
  });

  function handleFiles(files, area) {
    const list = area.querySelector('.file-list') || (() => {
      const ul = document.createElement('ul');
      ul.className = 'file-list list-unstyled mt-2';
      area.appendChild(ul);
      return ul;
    })();
    list.innerHTML = '';
    [...files].forEach(f => {
      const li = document.createElement('li');
      li.className = 'text-sm d-flex align-items-center gap-2 py-1';
      li.innerHTML = `<i class="bi bi-file-earmark text-primary"></i> <span>${f.name}</span> <small class="text-muted">(${(f.size/1024).toFixed(1)} KB)</small>`;
      list.appendChild(li);
    });
  }
}

// ── 9. CALENDAR WIDGET ───────────────────────
function initCalendar() {
  const widgets = $$('[data-calendar]');
  widgets.forEach(w => {
    renderCalendar(w, new Date());
  });
}

function renderCalendar(container, date) {
  const year = date.getFullYear();
  const month = date.getMonth();
  const today = new Date();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const days = ['Su','Mo','Tu','We','Th','Fr','Sa'];

  let html = `
    <div class="calendar-widget">
      <div class="calendar-nav">
        <button class="btn btn-sm btn-icon border-0" id="cal-prev"><i class="bi bi-chevron-left"></i></button>
        <strong>${monthNames[month]} ${year}</strong>
        <button class="btn btn-sm btn-icon border-0" id="cal-next"><i class="bi bi-chevron-right"></i></button>
      </div>
      <div class="calendar-grid">
        ${days.map(d => `<div class="calendar-day-header">${d}</div>`).join('')}
        ${Array(firstDay).fill('<div></div>').join('')}
  `;

  for (let d = 1; d <= daysInMonth; d++) {
    const isToday = d === today.getDate() && month === today.getMonth() && year === today.getFullYear();
    const hasEvent = [3, 8, 15, 22, 28].includes(d);
    html += `<div class="calendar-day ${isToday ? 'today' : ''} ${hasEvent ? 'has-event' : ''}">${d}</div>`;
  }

  html += '</div></div>';
  container.innerHTML = html;

  on($('#cal-prev', container), 'click', () => {
    const prev = new Date(year, month - 1, 1);
    renderCalendar(container, prev);
  });
  on($('#cal-next', container), 'click', () => {
    const next = new Date(year, month + 1, 1);
    renderCalendar(container, next);
  });
}

// ── 10. TOASTS ──────────────────────────────
function initToasts() {
  // Auto-show any .toast-auto elements
  $$('.toast-auto').forEach(el => {
    const toast = new bootstrap.Toast(el, { delay: 4000 });
    toast.show();
  });
}

window.showToast = function(msg, type = 'info') {
  const container = document.getElementById('toast-container') || (() => {
    const div = document.createElement('div');
    div.id = 'toast-container';
    div.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    div.style.zIndex = 9999;
    document.body.appendChild(div);
    return div;
  })();

  const icons = { success: 'check-circle-fill', danger: 'x-circle-fill', warning: 'exclamation-triangle-fill', info: 'info-circle-fill' };
  const id = 'toast-' + Date.now();
  container.insertAdjacentHTML('beforeend', `
    <div id="${id}" class="toast align-items-center text-bg-${type} border-0" role="alert">
      <div class="d-flex">
        <div class="toast-body d-flex align-items-center gap-2">
          <i class="bi bi-${icons[type] || icons.info}"></i> ${msg}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    </div>
  `);
  const toast = new bootstrap.Toast(document.getElementById(id), { delay: 4000 });
  toast.show();
  document.getElementById(id).addEventListener('hidden.bs.toast', () => document.getElementById(id)?.remove());
};

// ── 11. QUIZ LOGIC ───────────────────────────
function initQuiz() {
  $$('.quiz-option').forEach(opt => {
    on(opt, 'click', () => {
      const group = opt.closest('.quiz-options');
      if (!group) return;
      $$('.quiz-option', group).forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
    });
  });

  // Timer
  const timerEl = document.getElementById('quizTimer');
  if (timerEl) {
    let seconds = parseInt(timerEl.dataset.seconds || '3600');
    const interval = setInterval(() => {
      seconds--;
      if (seconds <= 0) { clearInterval(interval); return; }
      const h = Math.floor(seconds / 3600);
      const m = Math.floor((seconds % 3600) / 60);
      const s = seconds % 60;
      timerEl.textContent = `${h > 0 ? h + ':' : ''}${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
      if (seconds < 300) timerEl.style.background = 'var(--danger)';
    }, 1000);
  }
}

// ── 12. CHAT AUTO-RESIZE ────────────────────
function initChatInput() {
  $$('.chat-input').forEach(ta => {
    on(ta, 'input', () => {
      ta.style.height = 'auto';
      ta.style.height = Math.min(ta.scrollHeight, 120) + 'px';
    });
  });
}

// ── 13. KANBAN ──────────────────────────────
function initKanban() {
  let dragging = null;

  $$('.kanban-card').forEach(card => {
    card.setAttribute('draggable', true);
    on(card, 'dragstart', () => { dragging = card; card.style.opacity = '.4'; });
    on(card, 'dragend', () => { dragging = null; card.style.opacity = ''; });
  });

  $$('.kanban-col').forEach(col => {
    on(col, 'dragover', e => { e.preventDefault(); col.style.background = 'var(--primary-soft)'; });
    on(col, 'dragleave', () => { col.style.background = ''; });
    on(col, 'drop', e => {
      e.preventDefault();
      col.style.background = '';
      if (dragging) col.appendChild(dragging);
    });
  });
}

// ── 14. SKELETON LOADERS ────────────────────
function initSkeletons() {
  $$('[data-skeleton]').forEach(el => {
    const delay = parseInt(el.dataset.skeleton || '1500');
    setTimeout(() => {
      el.classList.remove('skeleton');
      el.removeAttribute('data-skeleton');
    }, delay);
  });
}

// ── 15. AOS ANIMATION ───────────────────────
function initAOS() {
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 600, easing: 'ease-out-quad', once: true, offset: 60 });
  }
}

// ── 16. CHARTS ──────────────────────────────
function initCharts() {
  if (typeof ApexCharts === 'undefined') return;

  // Revenue Area Chart
  const revenueEl = document.getElementById('revenueChart');
  if (revenueEl) {
    new ApexCharts(revenueEl, {
      series: [{ name: 'Revenue', data: [3200,4100,3800,5200,4900,6300,5800,7100,6500,8200,7600,9400] }],
      chart: { type: 'area', height: 280, toolbar: { show: false }, sparkline: { enabled: false } },
      colors: ['#5046e5'],
      fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: .35, opacityTo: .05 } },
      stroke: { curve: 'smooth', width: 2.5 },
      xaxis: { categories: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], axisBorder: { show: false }, axisTicks: { show: false } },
      yaxis: { labels: { formatter: v => '$' + (v/1000).toFixed(1) + 'k' } },
      grid: { borderColor: '#e2e8f0', strokeDashArray: 4 },
      tooltip: { y: { formatter: v => '$' + v.toLocaleString() } },
      dataLabels: { enabled: false },
    }).render();
  }

  // Enrollment Donut
  const enrollEl = document.getElementById('enrollChart');
  if (enrollEl) {
    new ApexCharts(enrollEl, {
      series: [44, 28, 18, 10],
      labels: ['Web Dev', 'Design', 'Marketing', 'Others'],
      chart: { type: 'donut', height: 260 },
      colors: ['#5046e5','#0ea5e9','#f59e0b','#10b981'],
      plotOptions: { pie: { donut: { size: '65%' } } },
      legend: { position: 'bottom', fontSize: '12px' },
      dataLabels: { enabled: false },
    }).render();
  }

  // Student Progress Bar Chart
  const progressEl = document.getElementById('progressChart');
  if (progressEl) {
    new ApexCharts(progressEl, {
      series: [{ name: 'Completed', data: [78, 62, 90, 45, 85] }, { name: 'In Progress', data: [22, 38, 10, 55, 15] }],
      chart: { type: 'bar', height: 260, stacked: true, toolbar: { show: false } },
      plotOptions: { bar: { borderRadius: 4, horizontal: false } },
      colors: ['#5046e5','#e2e8f0'],
      xaxis: { categories: ['HTML/CSS','JavaScript','Python','React','Node.js'] },
      grid: { borderColor: '#e2e8f0', strokeDashArray: 4 },
      legend: { show: false },
      dataLabels: { enabled: false },
    }).render();
  }

  // Sparklines
  $$('[data-sparkline]').forEach(el => {
    const data = JSON.parse(el.dataset.sparkline);
    const color = el.dataset.color || '#5046e5';
    new ApexCharts(el, {
      series: [{ data }],
      chart: { type: 'line', height: 50, sparkline: { enabled: true } },
      colors: [color],
      stroke: { curve: 'smooth', width: 2 },
      tooltip: { fixed: { enabled: false }, x: { show: false } },
    }).render();
  });

  // Attendance Chart
  const attEl = document.getElementById('attendanceChart');
  if (attEl) {
    new ApexCharts(attEl, {
      series: [{ name: 'Present', data: [22, 19, 24, 21, 23, 20] }, { name: 'Absent', data: [3, 6, 1, 4, 2, 5] }],
      chart: { type: 'bar', height: 260, toolbar: { show: false } },
      plotOptions: { bar: { borderRadius: 4, columnWidth: '55%' } },
      colors: ['#10b981', '#ef4444'],
      xaxis: { categories: ['Jan','Feb','Mar','Apr','May','Jun'] },
      grid: { borderColor: '#e2e8f0', strokeDashArray: 4 },
      dataLabels: { enabled: false },
    }).render();
  }

  // Line chart for teacher analytics
  const lineEl = document.getElementById('analyticsLineChart');
  if (lineEl) {
    new ApexCharts(lineEl, {
      series: [
        { name: 'Students', data: [120,145,132,168,155,190,178,205,195,220,210,245] },
        { name: 'Revenue', data: [4500,5200,4800,6100,5700,7200,6800,7800,7200,8500,8000,9200] }
      ],
      chart: { type: 'line', height: 300, toolbar: { show: false } },
      colors: ['#5046e5','#f59e0b'],
      stroke: { curve: 'smooth', width: 2.5 },
      xaxis: { categories: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], axisBorder: { show: false } },
      yaxis: [
        { title: { text: 'Students' } },
        { opposite: true, title: { text: 'Revenue ($)' }, labels: { formatter: v => '$' + (v/1000).toFixed(1) + 'k' } }
      ],
      grid: { borderColor: '#e2e8f0', strokeDashArray: 4 },
      legend: { position: 'top' },
      dataLabels: { enabled: false },
    }).render();
  }
}

// ── UTILITY: Star Rating ─────────────────────
$$('[data-rating]').forEach(container => {
  const rating = parseFloat(container.dataset.rating);
  const max = 5;
  let html = '';
  for (let i = 1; i <= max; i++) {
    if (i <= Math.floor(rating)) html += '<i class="bi bi-star-fill text-warning"></i>';
    else if (i - 0.5 <= rating) html += '<i class="bi bi-star-half text-warning"></i>';
    else html += '<i class="bi bi-star text-warning"></i>';
  }
  container.innerHTML = html;
});

// ── UTILITY: Clipboard Copy ──────────────────
$$('[data-copy]').forEach(btn => {
  on(btn, 'click', () => {
    const target = $(btn.dataset.copy);
    if (target) {
      navigator.clipboard.writeText(target.textContent.trim()).then(() => {
        window.showToast('Copied to clipboard!', 'success');
      });
    }
  });
});
