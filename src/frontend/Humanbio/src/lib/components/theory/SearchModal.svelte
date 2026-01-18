<script>
    import { onMount } from "svelte";
    import { fade, scale } from "svelte/transition";

    let { tree = [], isOpen = $bindable(false) } = $props();
    let searchQuery = $state("");
    let inputEl;

    function flatten(nodes) {
        let result = [];
        for (const node of nodes) {
            if (node.isFolder) {
                result = [...result, ...flatten(node.children)];
            } else {
                result.push(node);
            }
        }
        return result;
    }

    let filteredItems = $derived.by(() => {
        if (!searchQuery) return [];
        const all = flatten(tree);
        return all.filter((item) =>
            item.title.toLowerCase().includes(searchQuery.toLowerCase()),
        );
    });

    function close() {
        isOpen = false;
        searchQuery = "";
    }

    function handleKeydown(e) {
        if (e.key === "Escape") close();
    }

    // Focus input on open
    $effect(() => {
        if (isOpen && inputEl) {
            inputEl.focus();
        }
    });

    onMount(() => {
        // Global shortcut CMD/CTRL + K
        window.addEventListener("keydown", (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === "k") {
                e.preventDefault();
                isOpen = !isOpen;
            }
        });
    });
</script>

{#if isOpen}
    <!-- Backdrop with liquid blur effect -->
    <div
        class="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] bg-black/40 backdrop-blur-md transition-all px-4"
        onclick={close}
        transition:fade={{ duration: 200 }}
    >
        <!-- Modal Content -->
        <div
            class="w-full max-w-2xl bg-fd-card/90 border border-fd-border rounded-[28px] shadow-2xl overflow-hidden flex flex-col max-h-[70vh] relative glass"
            onclick={(e) => e.stopPropagation()}
            transition:scale={{ start: 0.95, duration: 200 }}
        >
            <!-- Search Input -->
            <div
                class="flex items-center px-8 py-6 border-b border-fd-border bg-fd-primary/5"
            >
                <i
                    class="bx bx-search text-2xl text-fd-primary mr-4 animate-pulse"
                ></i>
                <input
                    bind:this={inputEl}
                    type="text"
                    bind:value={searchQuery}
                    placeholder="Bắt đầu tìm kiếm trong thư viện Humainbio..."
                    class="w-full bg-transparent text-xl text-fd-foreground placeholder-fd-muted font-bold outline-none"
                    onkeydown={handleKeydown}
                />
                <div
                    class="hidden sm:flex text-[10px] font-black text-fd-muted px-2 py-1 border border-fd-border rounded-lg bg-fd-background shadow-sm"
                >
                    ESC
                </div>
            </div>

            <!-- Results -->
            <div class="overflow-y-auto p-4 custom-scrollbar">
                {#if searchQuery}
                    {#each filteredItems as item}
                        <a
                            href={`/theory/${item.slug}`}
                            onclick={close}
                            class="flex items-center gap-4 p-4 rounded-[18px] hover:bg-fd-primary/10 hover:translate-x-1 group transition-all duration-300 mb-1 border border-transparent hover:border-fd-primary/20"
                        >
                            <div
                                class="w-10 h-10 rounded-xl bg-fd-primary/5 flex items-center justify-center text-fd-primary group-hover:bg-fd-primary group-hover:text-white transition-all shadow-inner"
                            >
                                <i class="bx bxs-file-blank text-xl"></i>
                            </div>
                            <div class="flex flex-col flex-1">
                                <span
                                    class="text-[15px] font-black text-fd-foreground group-hover:text-fd-primary transition-colors"
                                    >{item.title}</span
                                >
                                <span
                                    class="text-[11px] font-bold text-fd-muted opacity-60 uppercase tracking-wider"
                                    >Bài học lý thuyết</span
                                >
                            </div>
                            <i
                                class="bx bx-chevron-right text-fd-muted group-hover:text-fd-primary opacity-0 group-hover:opacity-100 transition-all text-xl"
                            ></i>
                        </a>
                    {/each}
                    {#if filteredItems.length === 0}
                        <div class="py-16 text-center space-y-4">
                            <i
                                class="bx bx-search-alt text-5xl text-fd-muted opacity-20"
                            ></i>
                            <p class="text-fd-muted font-bold">
                                Không tìm thấy kết quả cho "<span
                                    class="text-fd-primary">{searchQuery}</span
                                >"
                            </p>
                        </div>
                    {/if}
                {:else}
                    <div class="py-16 text-center space-y-4 opacity-50">
                        <i
                            class="bx bx-keyboard text-5xl text-fd-primary animate-bounce"
                        ></i>
                        <p
                            class="text-fd-muted font-black uppercase tracking-widest text-[11px]"
                        >
                            Khởi tạo thành công... Start Typing
                        </p>
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}
