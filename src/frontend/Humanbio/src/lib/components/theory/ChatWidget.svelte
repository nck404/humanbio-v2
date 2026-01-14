<script>
    import { fly, fade } from "svelte/transition";
    import { tick, onMount } from "svelte";

    let { isOpen = $bindable(false), theme = "dark" } = $props();

    let messages = $state([
        {
            role: "assistant",
            content:
                "Hello! How can I help you with your biology studies today?",
        },
    ]);
    let inputValue = $state("");
    let chatContainer;

    // Draggable State
    let position = $state({ x: 0, y: 0 });
    let isDragging = $state(false);
    let dragOffset = { x: 0, y: 0 };
    let windowElement;

    function close() {
        isOpen = false;
    }

    onMount(() => {
        if (typeof window !== "undefined") {
            // Default position: Bottom Right
            position = {
                x: window.innerWidth - 370, // 350px width + 20px padding
                y: window.innerHeight - 520, // 500px height + 20px padding
            };
        }
    });

    function startDrag(e) {
        if (!windowElement) return;
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
            x: e.clientX - dragOffset.x,
            y: e.clientY - dragOffset.y,
        };
    }

    function stopDrag() {
        isDragging = false;
        window.removeEventListener("mousemove", handleDrag);
        window.removeEventListener("mouseup", stopDrag);
    }

    async function sendMessage() {
        if (!inputValue.trim()) return;

        messages = [...messages, { role: "user", content: inputValue }];
        inputValue = "";

        await tick();
        scrollToBottom();

        setTimeout(async () => {
            messages = [
                ...messages,
                {
                    role: "assistant",
                    content:
                        "This is a mock response. The backend is not connected yet.",
                },
            ];
            await tick();
            scrollToBottom();
        }, 1000);
    }

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
</script>

{#if isOpen}
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <div class="fixed inset-0 z-50 pointer-events-none">
        <!-- Chat Window -->
        <div
            bind:this={windowElement}
            style="left: {position.x}px; top: {position.y}px;"
            transition:fly={{ y: 20, duration: 300 }}
            class="hidden sm:flex fixed pointer-events-auto w-[380px] h-[550px] border border-fd-border rounded-[24px] shadow-2xl flex-col overflow-hidden glass ring-1 ring-fd-primary/5
            bg-fd-card/90"
        >
            <!-- Header (Draggable) -->
            <div
                onmousedown={startDrag}
                class="flex items-center justify-between px-5 py-4 border-b border-fd-border select-none h-14 cursor-grab active:cursor-grabbing bg-fd-primary/5"
            >
                <div class="flex items-center gap-3 pointer-events-none">
                    <div
                        class="w-2.5 h-2.5 rounded-full bg-fd-primary shadow-[0_0_10px_var(--primary-glow)] animate-pulse"
                    ></div>
                    <div class="flex flex-col">
                        <span
                            class="font-black text-[11px] tracking-widest uppercase text-fd-primary"
                            >Bio Assistant</span
                        >
                        <span
                            class="text-[9px] font-bold text-fd-muted opacity-60"
                            >AI Intelligence Core</span
                        >
                    </div>
                </div>
                <button
                    onmousedown={(e) => e.stopPropagation()}
                    onclick={close}
                    class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-fd-primary/10 text-fd-muted hover:text-fd-primary transition-all"
                    aria-label="Close"
                >
                    <i class="bx bx-x text-xl"></i>
                </button>
            </div>

            <!-- Messages Area -->
            <div
                bind:this={chatContainer}
                class="flex-1 overflow-y-auto p-5 flex flex-col gap-4 custom-scrollbar bg-fd-background/30"
            >
                {#each messages as msg}
                    <div
                        class="flex gap-3 {msg.role === 'user'
                            ? 'flex-row-reverse'
                            : ''}"
                    >
                        <div class="max-w-[85%] animate-fade-in">
                            <div
                                class="px-4 py-3 rounded-2xl text-[13px] leading-relaxed border
                                {msg.role === 'user'
                                    ? 'bg-fd-primary text-white border-fd-primary shadow-lg shadow-fd-primary/20 font-medium'
                                    : 'bg-fd-secondary border-fd-border text-fd-foreground font-medium'}"
                            >
                                {msg.content}
                            </div>
                            <div
                                class="mt-1 px-1 text-[9px] font-bold text-fd-muted uppercase tracking-tighter opacity-50 {msg.role ===
                                'user'
                                    ? 'text-right'
                                    : ''}"
                            >
                                {msg.role === "assistant"
                                    ? "Intelligence"
                                    : "Researcher"}
                            </div>
                        </div>
                    </div>
                {/each}
            </div>

            <!-- Input Area -->
            <div class="p-4 border-t border-fd-border bg-fd-card/50">
                <div
                    class="relative flex items-center gap-2 bg-fd-background border border-fd-border rounded-xl px-4 py-3 shadow-inner group focus-within:border-fd-primary/50 transition-all"
                >
                    <i
                        class="bx bx-chevron-right text-fd-primary font-bold group-focus-within:translate-x-1 transition-transform"
                    ></i>
                    <input
                        bind:value={inputValue}
                        onkeydown={handleKeydown}
                        placeholder="Ask anything about biology..."
                        class="w-full bg-transparent border-none text-[13px] text-fd-foreground placeholder:text-fd-muted placeholder:opacity-50 focus:ring-0 p-0 font-medium"
                        autocomplete="off"
                    />
                    <button
                        onclick={sendMessage}
                        class="p-1.5 rounded-lg bg-fd-primary/10 text-fd-primary hover:bg-fd-primary hover:text-white transition-all"
                    >
                        <i class="bx bxs-send"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile UI (Streamlined) -->
        <div
            class="sm:hidden fixed inset-0 flex items-end justify-center pointer-events-none"
        >
            <div
                transition:fly={{ y: 200, duration: 300 }}
                class="pointer-events-auto w-full h-[70vh] border-t border-fd-border rounded-t-[32px] shadow-2xl flex flex-col overflow-hidden bg-fd-card glass"
            >
                <div
                    class="w-12 h-1 bg-fd-border rounded-full mx-auto mt-3 mb-1"
                ></div>
                <!-- Mobile Header -->
                <div
                    class="flex items-center justify-between px-6 py-4 border-b border-fd-border bg-fd-primary/5"
                >
                    <div class="flex items-center gap-3">
                        <div
                            class="w-2.5 h-2.5 rounded-full bg-fd-primary animate-pulse shadow-[0_0_10px_var(--primary-glow)]"
                        ></div>
                        <span
                            class="font-black text-xs text-fd-primary tracking-widest uppercase"
                            >Assistant</span
                        >
                    </div>
                    <button
                        onclick={close}
                        class="w-10 h-10 flex items-center justify-center rounded-full bg-fd-accent text-fd-muted"
                    >
                        <i class="bx bx-x text-2xl"></i>
                    </button>
                </div>

                <div class="flex-1 overflow-y-auto p-6 flex flex-col gap-4">
                    {#each messages as msg}
                        <div
                            class="flex gap-3 {msg.role === 'user'
                                ? 'flex-row-reverse'
                                : ''}"
                        >
                            <div class="max-w-[85%]">
                                <div
                                    class="px-4 py-3 rounded-2xl text-[14px] leading-relaxed border
                                    {msg.role === 'user'
                                        ? 'bg-fd-primary text-white border-fd-primary shadow-lg shadow-fd-primary/20'
                                        : 'bg-fd-secondary border-fd-border text-fd-foreground font-medium'}"
                                >
                                    {msg.content}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
                <div class="p-4 border-t border-fd-border bg-fd-card pb-safe">
                    <div
                        class="relative flex items-center gap-3 bg-fd-background border border-fd-border rounded-2xl px-4 py-3"
                    >
                        <input
                            bind:value={inputValue}
                            onkeydown={handleKeydown}
                            placeholder="Type a message..."
                            class="w-full bg-transparent border-none text-[15px] text-fd-foreground focus:ring-0 p-0"
                            autocomplete="off"
                        />
                        <button
                            onclick={sendMessage}
                            class="w-10 h-10 flex items-center justify-center rounded-xl bg-fd-primary text-white shadow-lg shadow-fd-primary/20"
                        >
                            <i class="bx bxs-send text-xl"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}
