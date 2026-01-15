<script>
    import { fly, fade } from "svelte/transition";
    import { tick, onMount } from "svelte";

    let { isOpen = $bindable(false), theme = "dark" } = $props();

    // Chat State
    let sessions = $state([]);
    let currentSessionId = $state(null);
    let messages = $state([]);
    let inputValue = $state("");
    let chatContainer;
    let isLoading = $state(false);

    // Draggable & Resizable State
    let position = $state({ x: 0, y: 0 });
    let size = $state({ width: 420, height: 600 });
    let isDragging = $state(false);
    let isResizing = $state(false);
    let dragOffset = { x: 0, y: 0 };
    let resizeStart = { x: 0, y: 0, width: 0, height: 0 };
    let windowElement;
    let isRecording = $state(false);
    let recognition;
    let autoPlayVoice = $state(true);

    const API_BASE = "http://localhost:5000/api";

    function close() {
        isOpen = false;
    }

    onMount(() => {
        if (typeof window !== "undefined") {
            // Default position: Bottom Right
            position = {
                x: window.innerWidth - size.width - 40,
                y: window.innerHeight - size.height - 40,
            };
            loadSessions();

            // Initialize Speech Recognition
            const SpeechRecognition =
                window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRecognition) {
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.lang = "vi-VN";
                recognition.interimResults = false;

                recognition.onstart = () => {
                    isRecording = true;
                };

                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    inputValue = transcript;
                    sendMessage();
                };

                recognition.onerror = (event) => {
                    console.error("Speech recognition error:", event.error);
                    isRecording = false;
                };

                recognition.onend = () => {
                    isRecording = false;
                };
            }
        }
    });

    function toggleRecording() {
        if (!recognition) {
            alert("Speech recognition is not supported in this browser.");
            return;
        }
        if (isRecording) {
            recognition.stop();
        } else {
            recognition.start();
        }
    }

    function speak(text) {
        if (!text) return;

        // Stop any current speaking
        window.speechSynthesis.cancel();

        // Use our new backend TTS endpoint for high-quality Vietnamese voice
        const url = `${API_BASE}/chat/tts?text=${encodeURIComponent(text)}`;
        const audio = new Audio(url);
        audio.play().catch((e) => {
            console.error("Audio playback failed:", e);
            // Fallback to Web Speech API if backend fails
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "vi-VN";
            window.speechSynthesis.speak(utterance);
        });
    }

    // ============ API Functions ============
    async function loadSessions() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`${API_BASE}/chat/sessions`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (response.ok) {
                sessions = await response.json();
                if (sessions.length > 0 && !currentSessionId) {
                    currentSessionId = sessions[0].id;
                    await loadMessages(currentSessionId);
                }
            }
        } catch (error) {
            console.error("Failed to load sessions:", error);
        }
    }

    async function loadMessages(sessionId) {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(
                `${API_BASE}/chat/session/${sessionId}`,
                {
                    headers: { Authorization: `Bearer ${token}` },
                },
            );
            if (response.ok) {
                messages = await response.json();
                await tick();
                scrollToBottom();
            }
        } catch (error) {
            console.error("Failed to load messages:", error);
        }
    }

    async function createNewChat() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`${API_BASE}/chat/session`, {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` },
            });
            if (response.ok) {
                const newSession = await response.json();
                sessions = [newSession, ...sessions];
                currentSessionId = newSession.id;
                messages = [];
            }
        } catch (error) {
            console.error("Failed to create new chat:", error);
        }
    }

    async function sendMessage() {
        if (!inputValue.trim() || isLoading) return;

        // Create new session if none exists
        if (!currentSessionId) {
            await createNewChat();
        }

        const userMessage = inputValue;
        inputValue = "";
        isLoading = true;

        // Optimistically add user message
        messages = [...messages, { role: "user", content: userMessage }];
        await tick();
        scrollToBottom();

        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`${API_BASE}/chat/message`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    session_id: currentSessionId,
                    content: userMessage,
                }),
            });

            if (response.ok) {
                const aiMessage = await response.json();
                messages = [...messages, aiMessage];
                await tick();
                scrollToBottom();

                // Reload sessions to update title
                await loadSessions();

                if (autoPlayVoice) {
                    speak(aiMessage.content);
                }
            } else {
                messages = [
                    ...messages,
                    {
                        role: "model",
                        content:
                            "Sorry, I encountered an error. Please try again.",
                    },
                ];
            }
        } catch (error) {
            console.error("Failed to send message:", error);
            messages = [
                ...messages,
                {
                    role: "model",
                    content: "Network error. Please check your connection.",
                },
            ];
        } finally {
            isLoading = false;
        }
    }

    // ============ UI Functions ============
    function scrollToBottom() {
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }

    function handleKeydown(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    function copyMessage(content) {
        navigator.clipboard.writeText(content);
        // Could add a toast notification here
    }

    async function switchSession(sessionId) {
        currentSessionId = sessionId;
        await loadMessages(sessionId);
    }

    async function deleteSession(sessionId) {
        if (!confirm("Bạn có chắc muốn xóa cuộc trò chuyện này?")) return;

        try {
            const token = localStorage.getItem("token");
            const response = await fetch(
                `${API_BASE}/chat/session/${sessionId}`,
                {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${token}` },
                },
            );

            if (response.ok) {
                // Remove from sessions list
                sessions = sessions.filter((s) => s.id !== sessionId);

                // If deleted current session, switch to first available or clear
                if (currentSessionId === sessionId) {
                    if (sessions.length > 0) {
                        currentSessionId = sessions[0].id;
                        await loadMessages(currentSessionId);
                    } else {
                        currentSessionId = null;
                        messages = [];
                    }
                }
            }
        } catch (error) {
            console.error("Failed to delete session:", error);
        }
    }

    // ============ Drag & Resize ============
    function startDrag(e) {
        if (!windowElement || isResizing) return;
        isDragging = true;
        const rect = windowElement.getBoundingClientRect();
        dragOffset = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
        };

        window.addEventListener("mousemove", handleDrag);
        window.addEventListener("mouseup", stopDrag);
    }

    function handleDrag(e) {
        if (!isDragging) return;
        position = {
            x: Math.max(
                0,
                Math.min(
                    e.clientX - dragOffset.x,
                    window.innerWidth - size.width,
                ),
            ),
            y: Math.max(
                0,
                Math.min(
                    e.clientY - dragOffset.y,
                    window.innerHeight - size.height,
                ),
            ),
        };
    }

    function stopDrag() {
        isDragging = false;
        window.removeEventListener("mousemove", handleDrag);
        window.removeEventListener("mouseup", stopDrag);
    }

    function startResize(e) {
        e.stopPropagation();
        isResizing = true;
        resizeStart = {
            x: e.clientX,
            y: e.clientY,
            width: size.width,
            height: size.height,
        };

        window.addEventListener("mousemove", handleResize);
        window.addEventListener("mouseup", stopResize);
    }

    function handleResize(e) {
        if (!isResizing) return;
        const deltaX = e.clientX - resizeStart.x;
        const deltaY = e.clientY - resizeStart.y;

        size = {
            width: Math.max(
                320,
                Math.min(
                    resizeStart.width + deltaX,
                    window.innerWidth - position.x,
                ),
            ),
            height: Math.max(
                400,
                Math.min(
                    resizeStart.height + deltaY,
                    window.innerHeight - position.y,
                ),
            ),
        };
    }

    function stopResize() {
        isResizing = false;
        window.removeEventListener("mousemove", handleResize);
        window.removeEventListener("mouseup", stopResize);
    }
</script>

{#if isOpen}
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <div class="fixed inset-0 z-50 pointer-events-none">
        <!-- Chat Window -->
        <div
            bind:this={windowElement}
            style="left: {position.x}px; top: {position.y}px; width: {size.width}px; height: {size.height}px;"
            transition:fly={{ y: 20, duration: 300 }}
            class="hidden sm:flex fixed pointer-events-auto border border-fd-border rounded-2xl shadow-2xl flex-col overflow-hidden glass ring-1 ring-fd-primary/5 bg-fd-card/95 backdrop-blur-xl"
        >
            <!-- Header (Draggable) -->
            <div
                onmousedown={startDrag}
                class="flex items-center justify-between px-4 py-2.5 border-b border-fd-border select-none cursor-grab active:cursor-grabbing bg-fd-primary/5"
            >
                <div class="flex items-center gap-2 pointer-events-none">
                    <div
                        class="w-2 h-2 rounded-full bg-fd-primary shadow-[0_0_8px_var(--primary-glow)] animate-pulse"
                    ></div>
                    <div class="flex flex-col">
                        <span
                            class="font-bold text-[10px] tracking-wider uppercase text-fd-primary"
                        >
                            Bio AI
                        </span>
                    </div>
                </div>
                <div class="flex items-center gap-1">
                    <button
                        onmousedown={(e) => e.stopPropagation()}
                        onclick={() => (autoPlayVoice = !autoPlayVoice)}
                        class="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-fd-primary/10 {autoPlayVoice
                            ? 'text-fd-primary'
                            : 'text-fd-muted'} transition-all"
                        title={autoPlayVoice
                            ? "Auto-play: On"
                            : "Auto-play: Off"}
                    >
                        <i
                            class="bx {autoPlayVoice
                                ? 'bx-volume-full'
                                : 'bx-volume-mute'} text-lg"
                        ></i>
                    </button>
                    <button
                        onmousedown={(e) => e.stopPropagation()}
                        onclick={createNewChat}
                        class="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-fd-primary/10 text-fd-muted hover:text-fd-primary transition-all"
                        title="New Chat"
                    >
                        <i class="bx bx-plus text-lg"></i>
                    </button>
                    <button
                        onmousedown={(e) => e.stopPropagation()}
                        onclick={close}
                        class="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-fd-primary/10 text-fd-muted hover:text-fd-primary transition-all"
                        aria-label="Close"
                    >
                        <i class="bx bx-x text-lg"></i>
                    </button>
                </div>
            </div>

            <div class="flex flex-1 overflow-hidden">
                <!-- Sidebar - Chat History -->
                <div
                    class="w-48 border-r border-fd-border bg-fd-background/30 flex flex-col overflow-hidden"
                >
                    <div class="p-2 border-b border-fd-border">
                        <button
                            onclick={createNewChat}
                            class="w-full px-3 py-2 text-xs font-medium bg-fd-primary/10 hover:bg-fd-primary/20 text-fd-primary rounded-lg transition-all flex items-center justify-center gap-2"
                        >
                            <i class="bx bx-plus"></i>
                            New Chat
                        </button>
                    </div>
                    <div
                        class="flex-1 overflow-y-auto custom-scrollbar p-2 space-y-1"
                    >
                        {#each sessions as session}
                            <div class="relative group">
                                <button
                                    onclick={() => switchSession(session.id)}
                                    class="w-full px-3 py-2 text-left text-xs rounded-lg transition-all {currentSessionId ===
                                    session.id
                                        ? 'bg-fd-primary/20 text-fd-primary font-medium'
                                        : 'hover:bg-fd-accent text-fd-muted'}"
                                >
                                    <div class="truncate pr-6">
                                        {session.title}
                                    </div>
                                    <div class="text-[9px] opacity-60 mt-0.5">
                                        {new Date(
                                            session.created_at,
                                        ).toLocaleDateString()}
                                    </div>
                                </button>
                                <button
                                    onclick={(e) => {
                                        e.stopPropagation();
                                        deleteSession(session.id);
                                    }}
                                    class="absolute right-2 top-1/2 -translate-y-1/2 w-6 h-6 flex items-center justify-center rounded-md opacity-0 group-hover:opacity-100 hover:bg-red-500/20 text-red-500 transition-all"
                                    title="Xóa chat"
                                >
                                    <i class="bx bx-trash text-sm"></i>
                                </button>
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Main Chat Area -->
                <div class="flex-1 flex flex-col overflow-hidden">
                    <!-- Messages Area -->
                    <div
                        bind:this={chatContainer}
                        class="flex-1 overflow-y-auto p-4 flex flex-col gap-3 custom-scrollbar bg-fd-background/20"
                    >
                        {#each messages as msg, i}
                            <div
                                class="flex gap-2 {msg.role === 'user'
                                    ? 'flex-row-reverse'
                                    : ''}"
                                transition:fade={{ duration: 200 }}
                            >
                                <div class="max-w-[85%] group">
                                    <div
                                        class="px-3 py-2 rounded-xl text-xs leading-relaxed border {msg.role ===
                                        'user'
                                            ? 'bg-fd-primary text-white border-fd-primary shadow-lg shadow-fd-primary/20 font-medium'
                                            : 'bg-fd-secondary border-fd-border text-fd-foreground'}"
                                    >
                                        {msg.content}
                                    </div>
                                    {#if msg.role === "model"}
                                        <div
                                            class="flex gap-1 mt-1 opacity-0 group-hover:opacity-100 transition-opacity"
                                        >
                                            <button
                                                onclick={() =>
                                                    copyMessage(msg.content)}
                                                class="px-2 py-0.5 text-[9px] text-fd-muted hover:text-fd-primary flex items-center gap-1"
                                                title="Copy"
                                            >
                                                <i class="bx bx-copy"></i> Copy
                                            </button>
                                            <button
                                                onclick={() =>
                                                    speak(msg.content)}
                                                class="px-2 py-0.5 text-[9px] text-fd-muted hover:text-fd-primary flex items-center gap-1"
                                                title="Nghe"
                                            >
                                                <i class="bx bx-volume-full"
                                                ></i> Nghe
                                            </button>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        {/each}
                        {#if isLoading}
                            <div class="flex gap-2" transition:fade>
                                <div class="max-w-[85%]">
                                    <div
                                        class="px-3 py-2 rounded-xl text-xs bg-fd-secondary border border-fd-border"
                                    >
                                        <div class="flex gap-1">
                                            <div
                                                class="w-2 h-2 bg-fd-primary rounded-full animate-bounce"
                                            ></div>
                                            <div
                                                class="w-2 h-2 bg-fd-primary rounded-full animate-bounce"
                                                style="animation-delay: 0.1s"
                                            ></div>
                                            <div
                                                class="w-2 h-2 bg-fd-primary rounded-full animate-bounce"
                                                style="animation-delay: 0.2s"
                                            ></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {/if}
                    </div>

                    <!-- Input Area -->
                    <div class="p-3 border-t border-fd-border bg-fd-card/50">
                        <div
                            class="relative flex items-center gap-2 bg-fd-background border border-fd-border rounded-xl px-3 py-2 shadow-inner group focus-within:border-fd-primary/50 transition-all"
                        >
                            <i
                                class="bx bx-chevron-right text-fd-primary text-sm group-focus-within:translate-x-0.5 transition-transform"
                            ></i>
                            <input
                                bind:value={inputValue}
                                onkeydown={handleKeydown}
                                placeholder="Ask anything..."
                                disabled={isLoading}
                                class="w-full bg-transparent border-none text-xs text-fd-foreground placeholder:text-fd-muted placeholder:opacity-50 focus:ring-0 p-0 font-medium disabled:opacity-50"
                                autocomplete="off"
                            />
                            <div class="flex items-center gap-1.5">
                                <button
                                    onclick={toggleRecording}
                                    class="p-1.5 rounded-lg transition-all {isRecording
                                        ? 'bg-red-500 text-white animate-pulse'
                                        : 'text-fd-muted hover:bg-fd-accent hover:text-fd-primary'}"
                                    title={isRecording
                                        ? "Đang nghe..."
                                        : "Nói chuyện"}
                                >
                                    <i
                                        class="bx {isRecording
                                            ? 'bx-stop'
                                            : 'bx-microphone'} text-sm"
                                    ></i>
                                </button>
                                <button
                                    onclick={sendMessage}
                                    disabled={isLoading || !inputValue.trim()}
                                    class="p-1.5 rounded-lg bg-fd-primary/10 text-fd-primary hover:bg-fd-primary hover:text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    <i class="bx bxs-send text-sm"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Resize Handle -->
            <div
                onmousedown={startResize}
                class="absolute bottom-0 right-0 w-4 h-4 cursor-nwse-resize opacity-0 hover:opacity-100 transition-opacity"
                title="Resize"
            >
                <i class="bx bx-move text-fd-muted text-xs"></i>
            </div>
        </div>

        <!-- Mobile UI -->
        <div
            class="sm:hidden fixed inset-0 flex items-end justify-center pointer-events-none"
        >
            <div
                transition:fly={{ y: 200, duration: 300 }}
                class="pointer-events-auto w-full h-[75vh] border-t border-fd-border rounded-t-3xl shadow-2xl flex flex-col overflow-hidden bg-fd-card glass"
            >
                <div
                    class="w-12 h-1 bg-fd-border rounded-full mx-auto mt-3 mb-1"
                ></div>
                <!-- Mobile Header -->
                <div
                    class="flex items-center justify-between px-5 py-3 border-b border-fd-border bg-fd-primary/5"
                >
                    <div class="flex items-center gap-2">
                        <div
                            class="w-2 h-2 rounded-full bg-fd-primary animate-pulse shadow-[0_0_8px_var(--primary-glow)]"
                        ></div>
                        <span
                            class="font-bold text-xs text-fd-primary tracking-wider uppercase"
                            >Bio AI</span
                        >
                    </div>
                    <div class="flex items-center gap-2">
                        <button
                            onclick={() => (autoPlayVoice = !autoPlayVoice)}
                            class="w-9 h-9 flex items-center justify-center rounded-full {autoPlayVoice
                                ? 'bg-fd-primary/20 text-fd-primary'
                                : 'bg-fd-accent text-fd-muted'}"
                        >
                            <i
                                class="bx {autoPlayVoice
                                    ? 'bx-volume-full'
                                    : 'bx-volume-mute'} text-xl"
                            ></i>
                        </button>
                        <button
                            onclick={createNewChat}
                            class="w-9 h-9 flex items-center justify-center rounded-full bg-fd-accent text-fd-primary"
                            aria-label="Tạo cuộc hội thoại mới"
                        >
                            <i class="bx bx-plus text-xl"></i>
                        </button>
                        <button
                            onclick={close}
                            class="w-9 h-9 flex items-center justify-center rounded-full bg-fd-accent text-fd-muted"
                        >
                            <i class="bx bx-x text-2xl"></i>
                        </button>
                    </div>
                </div>

                <div class="flex-1 overflow-y-auto p-5 flex flex-col gap-3">
                    {#each messages as msg}
                        <div
                            class="flex gap-2 {msg.role === 'user'
                                ? 'flex-row-reverse'
                                : ''}"
                        >
                            <div class="max-w-[85%]">
                                <div
                                    class="px-4 py-3 rounded-2xl text-sm leading-relaxed border {msg.role ===
                                    'user'
                                        ? 'bg-fd-primary text-white border-fd-primary shadow-lg shadow-fd-primary/20'
                                        : 'bg-fd-secondary border-fd-border text-fd-foreground'}"
                                >
                                    {msg.content}
                                </div>
                                {#if msg.role === "model"}
                                    <div class="flex gap-2 mt-1 px-1">
                                        <button
                                            onclick={() => speak(msg.content)}
                                            class="text-[10px] text-fd-muted flex items-center gap-1"
                                        >
                                            <i class="bx bx-volume-full"></i> Nghe
                                        </button>
                                        <button
                                            onclick={() =>
                                                copyMessage(msg.content)}
                                            class="text-[10px] text-fd-muted flex items-center gap-1"
                                        >
                                            <i class="bx bx-copy"></i> Copy
                                        </button>
                                    </div>
                                {/if}
                            </div>
                        </div>
                    {/each}
                    {#if isLoading}
                        <div class="flex gap-2">
                            <div
                                class="px-4 py-3 rounded-2xl bg-fd-secondary border border-fd-border"
                            >
                                <div class="flex gap-1">
                                    <div
                                        class="w-2 h-2 bg-fd-primary rounded-full animate-bounce"
                                    ></div>
                                    <div
                                        class="w-2 h-2 bg-fd-primary rounded-full animate-bounce"
                                        style="animation-delay: 0.1s"
                                    ></div>
                                    <div
                                        class="w-2 h-2 bg-fd-primary rounded-full animate-bounce"
                                        style="animation-delay: 0.2s"
                                    ></div>
                                </div>
                            </div>
                        </div>
                    {/if}
                </div>

                <div class="p-4 border-t border-fd-border bg-fd-card pb-safe">
                    <div
                        class="relative flex items-center gap-3 bg-fd-background border border-fd-border rounded-2xl px-4 py-3"
                    >
                        <input
                            bind:value={inputValue}
                            onkeydown={handleKeydown}
                            placeholder="Type a message..."
                            disabled={isLoading}
                            class="w-full bg-transparent border-none text-sm text-fd-foreground focus:ring-0 p-0 disabled:opacity-50"
                            autocomplete="off"
                        />
                        <button
                            onclick={toggleRecording}
                            class="p-2 rounded-xl {isRecording
                                ? 'bg-red-500 text-white animate-pulse'
                                : 'text-fd-muted bg-fd-accent'}"
                            aria-label={isRecording
                                ? "Dừng ghi âm"
                                : "Bắt đầu ghi âm"}
                        >
                            <i
                                class="bx {isRecording
                                    ? 'bx-stop'
                                    : 'bx-microphone'} text-xl"
                            ></i>
                        </button>
                        <button
                            onclick={sendMessage}
                            disabled={isLoading || !inputValue.trim()}
                            class="w-10 h-10 flex items-center justify-center rounded-xl bg-fd-primary text-white shadow-lg shadow-fd-primary/20 disabled:opacity-50"
                            aria-label="Gửi tin nhắn"
                        >
                            <i class="bx bxs-send text-lg"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: transparent;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: hsl(var(--fd-border));
        border-radius: 3px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
        background: hsl(var(--fd-primary) / 0.5);
    }

    .glass {
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
</style>
