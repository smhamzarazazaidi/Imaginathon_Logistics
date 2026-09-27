// WebSocket Client for real-time updates
class WebSocketClient {
    constructor(url) {
        this.url = url || 'ws://localhost:8000/ws';
        this.ws = null;
        this.reconnectInterval = 5000;
        this.maxReconnectAttempts = 10;
        this.reconnectAttempts = 0;
        this.subscriptions = new Set();
        this.eventHandlers = {};
        this.heartbeatInterval = null;
    }

    connect() {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
            this.startHeartbeat();
            this.resubscribe();
            this.emit('connected');
        };

        this.ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                this.handleMessage(message);
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.emit('error', error);
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.stopHeartbeat();
            this.emit('disconnected');
            
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                this.reconnectAttempts++;
                console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
                setTimeout(() => this.connect(), this.reconnectInterval);
            }
        };
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.stopHeartbeat();
    }

    startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                this.ws.send(JSON.stringify({ type: 'heartbeat' }));
            }
        }, 30000);
    }

    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }

    subscribe(resource, resourceId = null) {
        const subscription = { resource, resourceId };
        this.subscriptions.add(subscription);
        
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'subscribe',
                resource,
                resource_id: resourceId
            }));
        }
    }

    unsubscribe(resource, resourceId = null) {
        const subscription = { resource, resourceId };
        this.subscriptions.delete(subscription);
        
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'unsubscribe',
                resource,
                resource_id: resourceId
            }));
        }
    }

    resubscribe() {
        this.subscriptions.forEach(({ resource, resourceId }) => {
            this.ws.send(JSON.stringify({
                type: 'subscribe',
                resource,
                resource_id: resourceId
            }));
        });
    }

    on(event, handler) {
        if (!this.eventHandlers[event]) {
            this.eventHandlers[event] = [];
        }
        this.eventHandlers[event].push(handler);
    }

    off(event, handler) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event] = this.eventHandlers[event].filter(h => h !== handler);
        }
    }

    emit(event, data) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].forEach(handler => handler(data));
        }
    }

    handleMessage(message) {
        const { type, data } = message;
        
        // Emit specific event
        this.emit(type, data);
        
        // Also emit generic message event
        this.emit('message', message);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WebSocketClient;
}
