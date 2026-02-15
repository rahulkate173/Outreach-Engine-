const API_BASE = '/api';
let currentChatId = null;
const token = localStorage.getItem('token');

if (!token) {
    window.location.href = '/login';
}

// Load chats on page load
async function loadChats() {
    try {
        const response = await fetch(`${API_BASE}/history/chats`, {
            headers: {'Authorization': `Bearer ${token}`}
        });
        
        if (response.ok) {
            const data = await response.json();
            displayChats(data.chats);
        }
    } catch (error) {
        console.error('Error loading chats:', error);
    }
}

function displayChats(chats) {
    const chatList = document.getElementById('chatList');
    chatList.innerHTML = '';
    
    chats.forEach(chat => {
        const chatItem = document.createElement('div');
        chatItem.className = 'chat-item';
        chatItem.innerHTML = `
            <div><strong>${chat.preview}</strong></div>
            <small>${new Date(chat.created_at).toLocaleDateString()}</small>
        `;
        chatItem.onclick = () => loadChat(chat.chat_id);
        chatList.appendChild(chatItem);
    });
}

async function newChat() {
    try {
        const response = await fetch(`${API_BASE}/chat/create-chat`, {
            method: 'POST',
            headers: {'Authorization': `Bearer ${token}`}
        });
        
        if (response.ok) {
            const data = await response.json();
            currentChatId = data.chat_id;
            document.getElementById('messages').innerHTML = '';
            loadChats();
        }
    } catch (error) {
        console.error('Error creating chat:', error);
    }
}

async function loadChat(chatId) {
    try {
        const response = await fetch(`${API_BASE}/history/chat/${chatId}`, {
            headers: {'Authorization': `Bearer ${token}`}
        });
        
        if (response.ok) {
            const chat = await response.json();
            currentChatId = chatId;
            displayMessages(chat.messages);
        }
    } catch (error) {
        console.error('Error loading chat:', error);
    }
}

function displayMessages(messages) {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = '';
    
    messages.forEach(msg => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${msg.role}`;
        messageDiv.textContent = msg.content;
        messagesDiv.appendChild(messageDiv);
    });
    
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const recipientInput = document.getElementById('chatInput');
    const companyInput = document.getElementById('companyInput');
    const jobInput = document.getElementById('jobInput');
    
    const content = messageInput.value.trim();
    const recipient = recipientInput.value.trim();
    const company = companyInput.value.trim();
    const job = jobInput.value.trim();
    
    if (!content) return;
    
    if (!currentChatId) {
        await newChat();
    }
    
    try {
        const response = await fetch(`${API_BASE}/chat/message`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chat_id: currentChatId,
                content,
                recipient_name: recipient,
                company,
                job_title: job
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Add messages to display
            displayMessage('user', content);
            displayMessage('assistant', data.message);
            
            // Update quota
            updateQuota(data.quota_remaining);
            
            // Clear inputs
            messageInput.value = '';
            
            // Reload chats
            loadChats();
        }
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

function displayMessage(role, content) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function updateQuota(remaining) {
    try {
        const response = await fetch(`${API_BASE}/billing/quota`, {
            headers: {'Authorization': `Bearer ${token}`}
        });
        
        if (response.ok) {
            const quota = await response.json();
            document.getElementById('quotaStatus').textContent = 
                `${quota.remaining}/${quota.daily_limit} remaining`;
            document.getElementById('planBadge').textContent = quota.plan;
        }
    } catch (error) {
        console.error('Error updating quota:', error);
    }
}

function selectPlan(plan) {
    if (plan === 'FREE') {
        alert('Already on FREE plan');
        return;
    }
    fetch(`${API_BASE}/billing/upgrade`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({new_plan: plan})
    });
}

// Initialize
loadChats();
updateQuota(0);

// Keyboard shortcut for sending
document.getElementById('messageInput').addEventListener('keypress', (e) => {
    if (e.ctrlKey || e.metaKey) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    }
});