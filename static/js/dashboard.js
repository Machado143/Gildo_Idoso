document.addEventListener('DOMContentLoaded', function() {
    // Atualizar dados em tempo real via WebSocket
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/dashboard/`;
    
    const socket = new WebSocket(wsUrl);
    
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.type === 'nova_leitura') {
            atualizarLeituras(data);
        } else if (data.type === 'novo_alerta') {
            mostrarNotificacao(data.alerta);
        }
    };
    
    function mostrarNotificacao(alerta) {
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-danger border-0 position-fixed';
        toast.style.top = '20px';
        toast.style.right = '20px';
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <strong>🚨 ${alerta.nivel.toUpperCase()}</strong><br>
                    ${alerta.mensagem}
                </div>
                <button class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        document.body.appendChild(toast);
        new bootstrap.Toast(toast).show();
    }
});