/**
 * AutomateX - Full Admin CMS Controller
 * Supports 100% editing & management:
 * - Projects CRUD (GitHub & Render Live URLs)
 * - Work Experience CRUD (Company, Role, Dates, Bullet Points)
 * - Education CRUD (Degree, Institution, Dates, Grade, Honors)
 * - Skills Management (Compact Single Box)
 * - PDF Resume Upload & Viewer
 * - Profile & Passcode PIN
 * - Client Inquiries / Messages
 */

document.addEventListener('DOMContentLoaded', () => {
  initPinLogin();
  bindAdminTabs();
  bindModalHelpers();
  bindProjectManagement();
  bindExperienceManagement();
  bindEducationManagement();
  bindSkillsManagement();
  bindResumeUpload();
  bindProfileManagement();
});

/* ==========================================================================
   1. PIN Login / Logout
   ========================================================================== */
function initPinLogin() {
  const modal = document.getElementById('admin-lock-modal');
  const pinInput = document.getElementById('admin-pin-input');
  const unlockBtn = document.getElementById('admin-unlock-btn');
  const errorMsg = document.getElementById('auth-error-msg');
  const logoutBtn = document.getElementById('admin-logout-btn');

  const doUnlock = async () => {
    const pin = pinInput ? pinInput.value.trim() : '';
    if (!pin) return;

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pin })
      });
      const data = await res.json();

      if (res.ok && data.success) {
        if (modal) modal.style.display = 'none';
        adminToast('Admin dashboard unlocked! Welcome back, Akhil.');
        setTimeout(() => window.location.reload(), 300);
      } else {
        if (errorMsg) {
          errorMsg.textContent = data.detail || 'Incorrect PIN! Default is akhil123';
          errorMsg.style.display = 'block';
        }
        if (pinInput) {
          pinInput.value = '';
          pinInput.focus();
        }
      }
    } catch (e) {
      if (errorMsg) {
        errorMsg.textContent = 'Server error during login.';
        errorMsg.style.display = 'block';
      }
    }
  };

  if (unlockBtn) unlockBtn.addEventListener('click', doUnlock);
  if (pinInput) {
    pinInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') doUnlock();
    });
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      await fetch('/api/admin/logout', { method: 'POST' });
      window.location.reload();
    });
  }
}

/* ==========================================================================
   2. Admin Tabs Navigation
   ========================================================================== */
function bindAdminTabs() {
  const tabs = document.querySelectorAll('.admin-tab-btn');
  const sections = document.querySelectorAll('.admin-tab-content');

  // Activate tab from URL hash if available (e.g. #experience)
  const hash = window.location.hash.replace('#', '');
  if (hash) {
    const matchingTab = document.querySelector(`.admin-tab-btn[data-tab="${hash}"]`);
    if (matchingTab) {
      tabs.forEach(t => t.classList.remove('active'));
      sections.forEach(s => s.style.display = 'none');
      matchingTab.classList.add('active');
      const targetSec = document.getElementById(`tab-${hash}`);
      if (targetSec) targetSec.style.display = 'block';
    }
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      tabs.forEach(t => t.classList.remove('active'));
      sections.forEach(s => s.style.display = 'none');

      tab.classList.add('active');
      const activeSec = document.getElementById(`tab-${target}`);
      if (activeSec) activeSec.style.display = 'block';
      window.location.hash = target;
    });
  });
}

/* ==========================================================================
   3. Modal Utilities
   ========================================================================== */
window.closeModal = function(backdropId) {
  const backdrop = document.getElementById(backdropId);
  if (backdrop) backdrop.classList.add('hidden');
};

function bindModalHelpers() {
  // Close modals on clicking backdrop
  document.querySelectorAll('.admin-modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        backdrop.classList.add('hidden');
      }
    });
  });

  // Close active modal on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.admin-modal-backdrop:not(.hidden)').forEach(m => {
        m.classList.add('hidden');
      });
    }
  });
}

/* ==========================================================================
   4. Projects Management (CRUD)
   ========================================================================== */
function bindProjectManagement() {
  const openBtn = document.getElementById('open-add-project-modal');
  const backdrop = document.getElementById('project-modal-backdrop');
  const form = document.getElementById('project-modal-form');
  const title = document.getElementById('project-modal-title');
  const renderInput = document.getElementById('modal-project-render');
  const renderCheck = document.getElementById('modal-project-has-render');

  if (openBtn) {
    openBtn.addEventListener('click', () => {
      if (form) form.reset();
      document.getElementById('modal-project-id').value = '';
      if (title) title.textContent = 'Add New Project';
      if (backdrop) backdrop.classList.remove('hidden');
    });
  }

  if (renderInput && renderCheck) {
    renderInput.addEventListener('input', () => {
      if (renderInput.value.trim()) {
        renderCheck.checked = true;
      }
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const id = document.getElementById('modal-project-id').value;
      const titleVal = document.getElementById('modal-project-title').value.trim();
      const catSelect = document.getElementById('modal-project-category');
      const category = catSelect.value;
      const category_label = catSelect.selectedOptions[0].text;
      const description = document.getElementById('modal-project-desc').value.trim();
      const tech_stack = document.getElementById('modal-project-tech').value.trim();
      const github_url = document.getElementById('modal-project-github').value.trim();
      const render_url = document.getElementById('modal-project-render').value.trim();
      const has_render = renderCheck ? (renderCheck.checked && render_url.length > 0) : false;

      const payload = {
        title: titleVal,
        category,
        category_label,
        description,
        tech_stack,
        github_url,
        render_url,
        has_render
      };

      try {
        let res;
        if (id) {
          res = await fetch(`/api/projects/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        } else {
          res = await fetch('/api/projects', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        }

        const data = await res.json();
        if (res.ok && data.success) {
          adminToast(id ? 'Project updated successfully! 🚀' : 'New project added live! 🎉');
          closeModal('project-modal-backdrop');
          setTimeout(() => {
            window.location.hash = 'projects';
            window.location.reload();
          }, 350);
        } else {
          alert(data.detail || 'Could not save project.');
        }
      } catch (err) {
        alert('Error saving project: ' + err.message);
      }
    });
  }
}

window.openEditProject = async function(id) {
  try {
    const res = await fetch(`/api/projects/${id}`);
    const project = await res.json();
    if (!project) return;

    document.getElementById('modal-project-id').value = project.id;
    document.getElementById('modal-project-title').value = project.title || '';
    document.getElementById('modal-project-category').value = project.category || 'backend';
    document.getElementById('modal-project-desc').value = project.description || '';
    document.getElementById('modal-project-tech').value = (project.tech_stack || []).join(', ');
    document.getElementById('modal-project-github').value = project.github_url || '';
    document.getElementById('modal-project-render').value = project.render_url || '';
    document.getElementById('modal-project-has-render').checked = !!project.has_render;

    document.getElementById('project-modal-title').textContent = 'Edit Project: ' + project.title;
    document.getElementById('project-modal-backdrop').classList.remove('hidden');
  } catch (err) {
    alert('Error loading project: ' + err.message);
  }
};

window.deleteProject = async function(id) {
  if (!confirm('Are you sure you want to delete this project?')) return;

  try {
    const res = await fetch(`/api/projects/${id}`, { method: 'DELETE' });
    const data = await res.json();

    if (res.ok && data.success) {
      adminToast('Project deleted.');
      const card = document.getElementById(`card-proj-${id}`);
      if (card) card.remove();
    } else {
      alert(data.detail || 'Could not delete project.');
    }
  } catch (err) {
    alert('Error deleting project: ' + err.message);
  }
};

/* ==========================================================================
   5. Work Experience Management (CRUD)
   ========================================================================== */
function bindExperienceManagement() {
  const openBtn = document.getElementById('open-add-exp-modal');
  const backdrop = document.getElementById('exp-modal-backdrop');
  const form = document.getElementById('exp-modal-form');
  const title = document.getElementById('exp-modal-title');

  if (openBtn) {
    openBtn.addEventListener('click', () => {
      if (form) form.reset();
      document.getElementById('modal-exp-id').value = '';
      if (title) title.textContent = 'Add Work Experience';
      if (backdrop) backdrop.classList.remove('hidden');
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const id = document.getElementById('modal-exp-id').value;
      const company = document.getElementById('modal-exp-company').value.trim();
      const role = document.getElementById('modal-exp-role').value.trim();
      const location = document.getElementById('modal-exp-location').value.trim();
      const period = document.getElementById('modal-exp-period').value.trim();
      const badge = document.getElementById('modal-exp-badge').value.trim() || 'Full-Time';
      const points = document.getElementById('modal-exp-points').value.trim();

      const payload = { company, role, location, period, badge, points };

      try {
        let res;
        if (id) {
          res = await fetch(`/api/experience/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        } else {
          res = await fetch('/api/experience', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        }

        const data = await res.json();
        if (res.ok && data.success) {
          adminToast(id ? 'Experience updated successfully! 💼' : 'New experience record added! 🎉');
          closeModal('exp-modal-backdrop');
          setTimeout(() => {
            window.location.hash = 'experience';
            window.location.reload();
          }, 350);
        } else {
          alert(data.detail || 'Could not save experience.');
        }
      } catch (err) {
        alert('Error saving experience: ' + err.message);
      }
    });
  }
}

window.openEditExperience = async function(id) {
  try {
    const res = await fetch(`/api/experience/${id}`);
    const exp = await res.json();
    if (!exp) return;

    document.getElementById('modal-exp-id').value = exp.id;
    document.getElementById('modal-exp-company').value = exp.company || '';
    document.getElementById('modal-exp-role').value = exp.role || '';
    document.getElementById('modal-exp-location').value = exp.location || '';
    document.getElementById('modal-exp-period').value = exp.period || '';
    document.getElementById('modal-exp-badge').value = exp.badge || 'Full-Time';
    document.getElementById('modal-exp-points').value = (exp.points || []).join('\n');

    document.getElementById('exp-modal-title').textContent = 'Edit Experience: ' + exp.company;
    document.getElementById('exp-modal-backdrop').classList.remove('hidden');
  } catch (err) {
    alert('Error loading experience details: ' + err.message);
  }
};

window.deleteExperience = async function(id) {
  if (!confirm('Delete this work experience record?')) return;

  try {
    const res = await fetch(`/api/experience/${id}`, { method: 'DELETE' });
    const data = await res.json();

    if (res.ok && data.success) {
      adminToast('Experience deleted.');
      const card = document.getElementById(`card-exp-${id}`);
      if (card) card.remove();
    } else {
      alert(data.detail || 'Could not delete experience.');
    }
  } catch (err) {
    alert('Error deleting experience: ' + err.message);
  }
};

/* ==========================================================================
   6. Education Management (CRUD)
   ========================================================================== */
function bindEducationManagement() {
  const openBtn = document.getElementById('open-add-edu-modal');
  const backdrop = document.getElementById('edu-modal-backdrop');
  const form = document.getElementById('edu-modal-form');
  const title = document.getElementById('edu-modal-title');

  if (openBtn) {
    openBtn.addEventListener('click', () => {
      if (form) form.reset();
      document.getElementById('modal-edu-id').value = '';
      if (title) title.textContent = 'Add Education Record';
      if (backdrop) backdrop.classList.remove('hidden');
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const id = document.getElementById('modal-edu-id').value;
      const degree = document.getElementById('modal-edu-degree').value.trim();
      const institution = document.getElementById('modal-edu-institution').value.trim();
      const location = document.getElementById('modal-edu-location').value.trim();
      const period = document.getElementById('modal-edu-period').value.trim();
      const grade = document.getElementById('modal-edu-grade').value.trim();
      const highlights = document.getElementById('modal-edu-highlights').value.trim();

      const payload = { degree, institution, location, period, grade, highlights };

      try {
        let res;
        if (id) {
          res = await fetch(`/api/education/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        } else {
          res = await fetch('/api/education', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        }

        const data = await res.json();
        if (res.ok && data.success) {
          adminToast(id ? 'Education updated successfully! 🎓' : 'New education record added! 🎉');
          closeModal('edu-modal-backdrop');
          setTimeout(() => {
            window.location.hash = 'education';
            window.location.reload();
          }, 350);
        } else {
          alert(data.detail || 'Could not save education record.');
        }
      } catch (err) {
        alert('Error saving education: ' + err.message);
      }
    });
  }
}

window.openEditEducation = async function(id) {
  try {
    const res = await fetch(`/api/education/${id}`);
    const edu = await res.json();
    if (!edu) return;

    document.getElementById('modal-edu-id').value = edu.id;
    document.getElementById('modal-edu-degree').value = edu.degree || '';
    document.getElementById('modal-edu-institution').value = edu.institution || '';
    document.getElementById('modal-edu-location').value = edu.location || '';
    document.getElementById('modal-edu-period').value = edu.period || '';
    document.getElementById('modal-edu-grade').value = edu.grade || '';
    document.getElementById('modal-edu-highlights').value = edu.highlights || '';

    document.getElementById('edu-modal-title').textContent = 'Edit Education: ' + edu.degree;
    document.getElementById('edu-modal-backdrop').classList.remove('hidden');
  } catch (err) {
    alert('Error loading education details: ' + err.message);
  }
};

window.deleteEducation = async function(id) {
  if (!confirm('Delete this education record?')) return;

  try {
    const res = await fetch(`/api/education/${id}`, { method: 'DELETE' });
    const data = await res.json();

    if (res.ok && data.success) {
      adminToast('Education record deleted.');
      const card = document.getElementById(`card-edu-${id}`);
      if (card) card.remove();
    } else {
      alert(data.detail || 'Could not delete education record.');
    }
  } catch (err) {
    alert('Error deleting education: ' + err.message);
  }
};

/* ==========================================================================
   7. Skills Management (Compact Single Box)
   ========================================================================== */
function bindSkillsManagement() {
  const form = document.getElementById('fastapi-skills-form');
  const textarea = document.getElementById('skills-input-textarea');
  const previewContainer = document.getElementById('skills-preview-chips');

  if (!form || !textarea) return;

  // Real-time chip preview typing
  textarea.addEventListener('input', () => {
    if (!previewContainer) return;
    const raw = textarea.value.replace(/\r/g, '').replace(/\n/g, ',');
    const skills = raw.split(',').map(s => s.trim()).filter(Boolean);

    previewContainer.innerHTML = '';
    skills.forEach(sk => {
      const chip = document.createElement('span');
      chip.className = 'tech-chip highlight';
      chip.textContent = sk;
      previewContainer.appendChild(chip);
    });
  });

  // Submit
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const skills_text = textarea.value.trim();
    if (!skills_text) {
      alert('Please enter at least one skill.');
      return;
    }

    try {
      const res = await fetch('/api/skills', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skills_text })
      });

      const data = await res.json();
      if (res.ok && data.success) {
        adminToast('Technical skillset updated! ⚡');
        setTimeout(() => {
          window.location.hash = 'skills';
          window.location.reload();
        }, 500);
      } else {
        alert(data.detail || 'Could not save skills.');
      }
    } catch (err) {
      alert('Error updating skills: ' + err.message);
    }
  });
}

/* ==========================================================================
   8. PDF Resume Upload
   ========================================================================== */
function bindResumeUpload() {
  const form = document.getElementById('fastapi-resume-upload-form');
  const fileInput = document.getElementById('resume-file-input');
  const uploadBtn = document.getElementById('upload-resume-btn');

  if (!form || !fileInput) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!fileInput.files || fileInput.files.length === 0) {
      alert('Please choose a .pdf resume file to upload.');
      return;
    }

    const file = fileInput.files[0];
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      alert('Please select a valid PDF file (.pdf extension).');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    if (uploadBtn) {
      uploadBtn.disabled = true;
      uploadBtn.innerHTML = '<span>Uploading PDF... ⏳</span>';
    }

    try {
      const res = await fetch('/api/resume/upload', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();

      if (res.ok && data.success) {
        adminToast(`Resume PDF uploaded (${data.size_kb} KB)! Live at /resume 📄`);
        setTimeout(() => {
          window.location.hash = 'resume';
          window.location.reload();
        }, 700);
      } else {
        alert(data.detail || 'Failed to upload resume PDF.');
      }
    } catch (err) {
      alert('Error uploading PDF: ' + err.message);
    } finally {
      if (uploadBtn) {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<span>🚀 Upload &amp; Update Live Resume</span>';
      }
    }
  });
}

/* ==========================================================================
   9. Profile & PIN Management
   ========================================================================== */
function bindProfileManagement() {
  const form = document.getElementById('fastapi-profile-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('profile-name').value.trim();
    const brand = document.getElementById('profile-brand').value.trim();
    const role_title = document.getElementById('profile-role').value.trim();
    const tagline = document.getElementById('profile-tagline').value.trim();
    const email = document.getElementById('profile-email').value.trim();
    const phone = document.getElementById('profile-phone').value.trim();
    const location = document.getElementById('profile-location').value.trim();
    const status_badge = document.getElementById('profile-status').value.trim();
    const github = document.getElementById('profile-github').value.trim();
    const linkedin = document.getElementById('profile-linkedin').value.trim();
    const about = document.getElementById('profile-about').value.trim();
    const admin_pin = document.getElementById('profile-pin').value.trim();

    const payload = {
      name,
      brand,
      role_title,
      tagline,
      email,
      phone,
      location,
      status_badge,
      github,
      linkedin,
      about,
      admin_pin
    };

    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (res.ok && data.success) {
        adminToast('Profile and Security PIN updated successfully! ⚡');
      } else {
        alert(data.detail || 'Could not update profile.');
      }
    } catch (err) {
      alert('Error updating profile: ' + err.message);
    }
  });
}

/* ==========================================================================
   10. Inquiries & Messages
   ========================================================================== */
window.toggleMessageRead = async function(id) {
  try {
    const res = await fetch(`/api/messages/${id}/read`, { method: 'PUT' });
    const data = await res.json();
    if (res.ok && data.success) {
      const card = document.getElementById(`msg-card-${id}`);
      if (card) card.classList.toggle('unread');
      adminToast('Inquiry status updated.');
    }
  } catch (err) {
    console.error(err);
  }
};

window.deleteMessage = async function(id) {
  if (!confirm('Delete this inquiry?')) return;
  try {
    const res = await fetch(`/api/messages/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (res.ok && data.success) {
      const card = document.getElementById(`msg-card-${id}`);
      if (card) card.remove();
      adminToast('Inquiry deleted.');
    }
  } catch (err) {
    alert('Error deleting message: ' + err.message);
  }
};

/* ==========================================================================
   Toast Notification System
   ========================================================================== */
function adminToast(message) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>⚡</span><span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
