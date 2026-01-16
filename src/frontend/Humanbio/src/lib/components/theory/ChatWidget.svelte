<script>
    import { fly, fade } from "svelte/transition";
    import { tick, onMount, onDestroy } from "svelte";
    import { renderMarkdown } from "$lib/utils/markdown";
    import { auth } from "$lib/stores/auth";
    import Avatar from "$lib/components/common/Avatar.svelte";
    import { API_URL } from "$lib/constants";

    let { isOpen = $bindable(false) } = $props();

    // Chat State
    let conversations = $state([]);
    let activeConv = $state(null);
    let messages = $state([]);
    let inputValue = $state("");
    let chatContainer = $state();
    let isLoading = $state(false);
    let searchUserId = $state("");
    let eventSource;

    const API_BASE = `${API_URL}/api/messages`;

    // Draggable State
    let position = $state({ x: 0, y: 0 });
    let size = $state({ width: 420, height: 600 });
    let isDragging = $state(false);
    let dragOffset = { x: 0, y: 0 };

    onMount(() => {
        if (typeof window !== "undefined") {
            position = {
                x: window.innerWidth - size.width - 40,
                y: window.innerHeight - size.height - 40,
            };
            loadConversations();
            setupSSE();
        }
    });

    onDestroy(() => {
        if (eventSource) eventSource.close();
    });

    function setupSSE() {
        if (!eventSource && $auth.token) {
            eventSource = new EventSource(
                `${API_BASE}/stream?token=${$auth.token}`,
            );
            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleSSENotification(data);
            };
            eventSource.onerror = (err) => {
                console.error("SSE connection lost", err);
                eventSource.close();
                eventSource = null;
                // Retry after 5s
                setTimeout(setupSSE, 5000);
            };
        }
    }

    function handleSSENotification(data) {
        if (data.type === "new_message") {
            const { conversation_id, message } = data;

            // If it's the current conversation, add to messages
            if (activeConv && activeConv.id === conversation_id) {
                messages = [...messages, message];
                scrollToBottom();
            }

            // Refresh conversation list to update "last message"
            loadConversations();
        }
    }

    async function loadConversations() {
        try {
            const response = await fetch(`${API_BASE}/conversations`, {
                headers: { Authorization: `Bearer ${$auth.token}` },
            });
            if (response.ok) {
                conversations = await response.json();
            }
        } catch (err) {
            console.error("Failed to load conversations", err);
        }
    }

    async function selectConversation(conv) {
        activeConv = conv;
        messages = [];
        isLoading = true;
        try {
            const response = await fetch(
                `${API_BASE}/conversation/${conv.id}/messages`,
                {
                    headers: { Authorization: `Bearer ${$auth.token}` },
                },
            );
            if (response.ok) {
                messages = await response.json();
                scrollToBottom();
            }
        } catch (err) {
            console.error("Failed to load messages", err);
        } finally {
            isLoading = false;
        }
    }

    async function createByUserId() {
        if (!searchUserId) return;
        try {
            const response = await fetch(`${API_BASE}/conversation`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: JSON.stringify({ user_id: searchUserId }),
            });
            const data = await response.json();
            if (response.ok) {
                await loadConversations();
                const newConv = conversations.find((c) => c.id === data.id);
                if (newConv) selectConversation(newConv);
                searchUserId = "";
            } else {
                alert(data.error || "User not found");
            }
        } catch (err) {
            console.error("Failed to create conversation", err);
        }
    }

    async function sendMessage() {
        if (!inputValue.trim() || !activeConv) return;
        const currentInput = inputValue;
        inputValue = "";

        // Optimistic UI
        const tempMsg = {
            id: Date.now(),
            sender_id: $auth.user.id,
            content: currentInput,
            created_at: new Date().toISOString(),
        };
        messages = [...messages, tempMsg];
        scrollToBottom();

        try {
            const response = await fetch(`${API_BASE}/send`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: JSON.stringify({
                    conversation_id: activeConv.id,
                    content: currentInput,
                }),
            });
            if (response.ok) {
                const savedMsg = await response.json();
                // Replace temp message with actual saved message
                messages = messages.map((m) =>
                    m.id === tempMsg.id ? savedMsg : m,
                );
                loadConversations();
            }
        } catch (err) {
            console.error("Failed to send message", err);
        }
    }

    async function scrollToBottom() {
        await tick();
        if (chatContainer) {
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: "smooth",
            });
        }
    }

    // Draggable Logic
    function startDrag(e) {
        isDragging = true;
        dragOffset = {
            x: e.clientX - position.x,
            y: e.clientY - position.y,
        };
        window.addEventListener("mousemove", handleMouseMove);
        window.addEventListener("mouseup", stopDrag);
    }
    function handleMouseMove(e) {
        if (isDragging) {
            position = {
                x: e.clientX - dragOffset.x,
                y: e.clientY - dragOffset.y,
            };
        }
    }
    function stopDrag() {
        isDragging = false;
        window.removeEventListener("mousemove", handleMouseMove);
        window.removeEventListener("mouseup", stopDrag);
    }
</script>

{#if isOpen}
    <div
        class="fixed z-[200] glass border border-fd-border/50 shadow-2xl rounded-2xl flex flex-col overflow-hidden select-none"
        style="width: {size.width}px; height: {size.height}px; left: {position.x}px; top: {position.y}px;"
        transition:fly={{ y: 20, duration: 300 }}
    >
        <!-- Header -->
        <div
            class="bg-fd-background/80 p-3 flex items-center justify-between border-b border-fd-border cursor-move"
            onmousedown={startDrag}
            role="none"
        >
            <div class="flex items-center gap-3">
                <div
                    class="w-8 h-8 bg-fd-primary rounded-lg flex items-center justify-center shadow-lg"
                >
                    <i class="bx bx-chat text-white text-lg"></i>
                </div>
                <div class="flex flex-col">
                    <span
                        class="text-xs font-black text-fd-foreground tracking-tight"
                        >Human Chat</span
                    >
                    <span
                        class="text-[9px] font-bold text-fd-primary uppercase tracking-[0.2em] opacity-80"
                        >My ID: {$auth.user?.id}</span
                    >
                </div>
            </div>
            <div class="flex items-center gap-1">
                <button
                    onclick={() => (isOpen = false)}
                    class="w-7 h-7 rounded-lg hover:bg-fd-accent flex items-center justify-center transition-all text-fd-muted hover:text-fd-foreground"
                    aria-label="Đóng chat"
                    title="Đóng"
                >
                    <i class="bx bx-x text-lg"></i>
                </button>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <!-- Sidebar: Conversation List -->
            <div
                class="w-40 border-r border-fd-border bg-fd-background/30 flex flex-col"
            >
                <div class="p-2 border-b border-fd-border">
                    <div class="relative">
                        <input
                            type="text"
                            bind:value={searchUserId}
                            placeholder="Nhập ID kết bạn..."
                            class="w-full bg-fd-secondary border border-fd-border rounded-lg px-2 py-1.5 text-[10px] outline-none focus:ring-1 ring-fd-primary"
                            onkeydown={(e) =>
                                e.key === "Enter" && createByUserId()}
                        />
                        <button
                            onclick={createByUserId}
                            class="absolute right-1 top-1/2 -translate-y-1/2 text-fd-primary hover:scale-110 transition-transform p-1"
                            aria-label="Thêm bạn"
                            title="Thêm"
                        >
                            <i class="bx bx-plus text-sm"></i>
                        </button>
                    </div>
                </div>
                <div class="flex-1 overflow-y-auto custom-scrollbar">
                    {#each conversations as conv}
                        <button
                            onclick={() => selectConversation(conv)}
                            class="w-full p-2 flex items-center gap-2 hover:bg-fd-accent transition-all text-left border-b border-fd-border/30 {activeConv?.id ===
                            conv.id
                                ? 'bg-fd-primary/5 border-r-2 border-r-fd-primary'
                                : ''}"
                        >
                            <Avatar
                                url={conv.other_user.avatar_url}
                                seed={conv.other_user.avatar_seed ||
                                    conv.other_user.username}
                                size={28}
                                class="rounded-lg shrink-0"
                            />
                            <div class="flex-1 min-w-0">
                                <div
                                    class="text-[11px] font-bold text-fd-foreground truncate"
                                >
                                    {conv.other_user.username}
                                </div>
                                <div class="text-[9px] text-fd-muted truncate">
                                    {conv.last_message.content || "No messages"}
                                </div>
                            </div>
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Chat Area -->
            <div class="flex-1 flex flex-col bg-white/40">
                {#if activeConv}
                    <div
                        class="p-2 border-b border-fd-border flex items-center gap-2 bg-fd-background/40"
                    >
                        <Avatar
                            url={activeConv.other_user.avatar_url}
                            seed={activeConv.other_user.avatar_seed ||
                                activeConv.other_user.username}
                            size={24}
                            class="rounded-md"
                        />
                        <div class="text-[11px] font-black text-fd-foreground">
                            {activeConv.other_user.username}
                        </div>
                        <div class="ml-auto flex items-center gap-1">
                            <div
                                class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"
                            ></div>
                            <span
                                class="text-[9px] font-bold text-fd-muted uppercase tracking-widest"
                                >Trực tuyến</span
                            >
                        </div>
                    </div>

                    <div
                        bind:this={chatContainer}
                        class="flex-1 overflow-y-auto p-3 flex flex-col gap-2 custom-scrollbar"
                    >
                        {#each messages as msg}
                            <div
                                class="flex gap-2 {msg.sender_id ===
                                $auth.user.id
                                    ? 'flex-row-reverse'
                                    : ''}"
                            >
                                <div class="max-w-[80%]">
                                    <div
                                        class="px-2.5 py-1.5 rounded-xl text-[11px] leading-snug border {msg.sender_id ===
                                        $auth.user.id
                                            ? 'bg-fd-primary text-white border-fd-primary shadow-sm font-medium'
                                            : 'bg-fd-secondary border-fd-border text-fd-foreground shadow-sm'}"
                                    >
                                        {msg.content}
                                    </div>
                                    <span
                                        class="text-[8px] text-fd-muted mt-1 opacity-50 px-1 {msg.sender_id ===
                                        $auth.user.id
                                            ? 'text-right block'
                                            : ''}"
                                    >
                                        {new Date(
                                            msg.created_at,
                                        ).toLocaleTimeString([], {
                                            hour: "2-digit",
                                            minute: "2-digit",
                                        })}
                                    </span>
                                </div>
                            </div>
                        {/each}
                        {#if isLoading}
                            <div class="flex justify-center p-4">
                                <i
                                    class="bx bx-loader-alt animate-spin text-fd-primary"
                                ></i>
                            </div>
                        {/if}
                    </div>

                    <div
                        class="p-2 border-t border-fd-border bg-fd-background/40"
                    >
                        <div
                            class="flex items-end gap-2 bg-fd-secondary rounded-xl p-1.5 border border-fd-border/50"
                        >
                            <textarea
                                bind:value={inputValue}
                                placeholder="Viết tin nhắn..."
                                class="flex-1 bg-transparent border-none outline-none text-[11px] font-medium py-1 px-2 max-h-24 min-h-[22px] resize-none"
                                onkeydown={(e) => {
                                    if (e.key === "Enter" && !e.shiftKey) {
                                        e.preventDefault();
                                        sendMessage();
                                    }
                                }}
                            ></textarea>
                            <button
                                onclick={sendMessage}
                                class="w-8 h-8 rounded-lg bg-fd-primary text-white flex items-center justify-center hover:scale-105 transition-all shadow-lg active:scale-95 disabled:opacity-50"
                                disabled={!inputValue.trim()}
                                aria-label="Gửi tin nhắn"
                                title="Gửi (Enter)"
                            >
                                <i class="bx bxs-send"></i>
                            </button>
                        </div>
                    </div>
                {:else}
                    <div
                        class="flex-1 flex flex-col items-center justify-center p-8 text-center opacity-40"
                    >
                        <div
                            class="w-16 h-16 bg-fd-primary/10 rounded-full flex items-center justify-center mb-4"
                        >
                            <i
                                class="bx bx-message-square-dots text-3xl text-fd-primary"
                            ></i>
                        </div>
                        <h4
                            class="text-xs font-black text-fd-foreground mb-1 uppercase tracking-widest"
                        >
                            Bắt đầu trò chuyện
                        </h4>
                        <p
                            class="text-[10px] font-medium text-fd-muted leading-relaxed"
                        >
                            Nhập ID của người dùng khác ở cột bên trái<br />để
                            băt đầu kết nối và học tập cùng nhau.
                        </p>
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}

<style>
    .glass {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
    }
</style>
