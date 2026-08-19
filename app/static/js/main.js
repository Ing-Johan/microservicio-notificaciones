// API Base URL
const API_BASE_URL = '/notificaciones';

let targetDeleteId = null;

// Initialize Dashboard on Load
document.addEventListener('DOMContentLoaded', () => {
    cargarNotificaciones();
});

// Toast Alert System
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'fa-circle-check' : 'fa-triangle-exclamation';
    const color = type === 'success' ? '#34d399' : '#f87171';

    toast.innerHTML = `
        <i class="fa-solid ${icon}" style="color: ${color}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Dynamically Adjust Form Label based on Tipo (Email / SMS)
function handleTipoChange(tipo) {
    const lbl = document.getElementById('lblDestinatario');
    const input = document.getElementById('destinatario');

    if (tipo === 'sms') {
        lbl.innerHTML = '<i class="fa-solid fa-phone"></i> Destinatario (Teléfono / SMS)';
        input.placeholder = '+573001234567';
    } else {
        lbl.innerHTML = '<i class="fa-solid fa-at"></i> Destinatario (Email)';
        input.placeholder = 'ejemplo@correo.com';
    }
}

// 1. READ ALL / FILTER (GET /notificaciones)
async function cargarNotificaciones(destinatario = null) {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = `
        <tr>
            <td colspan="7" class="text-center py-4">
                <i class="fa-solid fa-spinner fa-spin"></i> Cargando datos...
            </td>
        </tr>
    `;

    try {
        let url = API_BASE_URL;
        if (destinatario && destinatario.trim() !== '') {
            url += `?destinatario=${encodeURIComponent(destinatario.trim())}`;
        }

        const response = await fetch(url);
        const notificaciones = await response.json();

        renderTable(notificaciones);
        updateMetrics(notificaciones);
    } catch (error) {
        console.error('Error al cargar notificaciones:', error);
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4 color-danger">
                    <i class="fa-solid fa-triangle-exclamation"></i> Error al conectar con el servidor
                </td>
            </tr>
        `;
        showToast('Error al conectar con la API del microservicio', 'error');
    }
}

// Render Table Rows
function renderTable(list) {
    const tableBody = document.getElementById('tableBody');

    if (!Array.isArray(list) || list.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4 color-muted">
                    <i class="fa-solid fa-inbox"></i> No hay notificaciones registradas.
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = list.map(n => {
        const isEmail = n.tipo === 'email';
        const tipoBadge = isEmail
            ? `<span class="badge-tipo email"><i class="fa-solid fa-envelope"></i> Email</span>`
            : `<span class="badge-tipo sms"><i class="fa-solid fa-comment-sms"></i> SMS</span>`;
        
        const fechaFormatted = n.fecha ? new Date(n.fecha).toLocaleString() : 'N/A';

        return `
            <tr>
                <td><strong>#${n.id}</strong></td>
                <td>${tipoBadge}</td>
                <td>${escapeHtml(n.destinatario)}</td>
                <td>${escapeHtml(n.asunto)}</td>
                <td><span class="badge-estado"><i class="fa-solid fa-check"></i> ${escapeHtml(n.estado_envio)}</span></td>
                <td class="color-muted text-sm">${fechaFormatted}</td>
                <td>
                    <div class="action-buttons">
                        <button class="action-btn edit" title="Editar (PUT)" onclick="openEditModal(${n.id})">
                            <i class="fa-solid fa-pen"></i>
                        </button>
                        <button class="action-btn delete" title="Eliminar (DELETE)" onclick="openDeleteModal(${n.id})">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// Update Dashboard Counter Cards
function updateMetrics(list) {
    if (!Array.isArray(list)) return;
    
    document.getElementById('statTotal').textContent = list.length;
    const emails = list.filter(n => n.tipo === 'email').length;
    const sms = list.filter(n => n.tipo === 'sms').length;
    
    document.getElementById('statEmail').textContent = emails;
    document.getElementById('statSms').textContent = sms;
}

// 2. CREATE (POST /notificaciones)
async function handleCreate(event) {
    event.preventDefault();
    const btnSubmit = document.getElementById('btnSubmit');
    btnSubmit.disabled = true;
    btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Enviando...';

    const payload = {
        tipo: document.getElementById('tipo').value,
        destinatario: document.getElementById('destinatario').value,
        asunto: document.getElementById('asunto').value,
        mensaje: document.getElementById('mensaje').value
    };

    try {
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.status === 201) {
            showToast(`¡Notificación #${data.id} creada y enviada exitosamente!`, 'success');
            document.getElementById('createForm').reset();
            handleTipoChange('email');
            cargarNotificaciones();
        } else {
            showToast(data.error || 'Error al crear la notificación', 'error');
        }
    } catch (error) {
        console.error('Error POST:', error);
        showToast('Error de red al procesar la solicitud', 'error');
    } finally {
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Simular Envío y Guardar';
    }
}

// 3. EDIT & UPDATE (PUT /notificaciones/<id>)
async function openEditModal(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/${id}`);
        if (!response.ok) throw new Error('No se pudo obtener el registro');
        
        const data = await response.json();
        
        document.getElementById('editId').value = data.id;
        document.getElementById('editModalIdTitle').textContent = `#${data.id}`;
        document.getElementById('editTipo').value = data.tipo;
        document.getElementById('editDestinatario').value = data.destinatario;
        document.getElementById('editAsunto').value = data.asunto;
        document.getElementById('editMensaje').value = data.mensaje;

        document.getElementById('editModal').classList.remove('hidden');
    } catch (error) {
        showToast('No se pudo cargar la notificación para edición', 'error');
    }
}

function closeEditModal() {
    document.getElementById('editModal').classList.add('hidden');
}

async function handleSaveEdit(event) {
    event.preventDefault();
    const id = document.getElementById('editId').value;
    
    const payload = {
        tipo: document.getElementById('editTipo').value,
        destinatario: document.getElementById('editDestinatario').value,
        asunto: document.getElementById('editAsunto').value,
        mensaje: document.getElementById('editMensaje').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            showToast(`Notificación #${id} actualizada exitosamente (PUT)`, 'success');
            closeEditModal();
            cargarNotificaciones();
        } else {
            showToast(data.error || 'Error al actualizar', 'error');
        }
    } catch (error) {
        showToast('Error de red al actualizar registro', 'error');
    }
}

// 4. DELETE (DELETE /notificaciones/<id>)
function openDeleteModal(id) {
    targetDeleteId = id;
    document.getElementById('deleteModalId').textContent = `#${id}`;
    document.getElementById('deleteModal').classList.remove('hidden');
}

function closeDeleteModal() {
    targetDeleteId = null;
    document.getElementById('deleteModal').classList.add('hidden');
}

async function confirmDelete() {
    if (!targetDeleteId) return;

    try {
        const response = await fetch(`${API_BASE_URL}/${targetDeleteId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            showToast(`Notificación #${targetDeleteId} eliminada permanentemente (DELETE)`, 'success');
            closeDeleteModal();
            cargarNotificaciones();
        } else {
            showToast(data.error || 'Error al eliminar', 'error');
        }
    } catch (error) {
        showToast('Error de red al eliminar el registro', 'error');
    }
}

// Filter Actions
function handleSearchFilter() {
    const val = document.getElementById('filterDestinatario').value;
    cargarNotificaciones(val);
}

function handleFilterKeyup(event) {
    if (event.key === 'Enter') {
        handleSearchFilter();
    }
}

function clearFilter() {
    document.getElementById('filterDestinatario').value = '';
    cargarNotificaciones();
}

// Utility: Escape HTML
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
