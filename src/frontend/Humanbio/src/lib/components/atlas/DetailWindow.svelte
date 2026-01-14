<script>
    import { fly, fade, scale } from "svelte/transition";
    import { createEventDispatcher } from "svelte";

    export let part = null; // The selected main part

    const dispatch = createEventDispatcher();
    let selectedSubPart = null;

    function close() {
        dispatch("close");
        selectedSubPart = null;
    }

    function selectSubPart(sub) {
        selectedSubPart = sub;
    }
</script>

{#if part}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center p-4 md:p-10"
        in:fade={{ duration: 200 }}
    >
        <!-- Backdrop -->
        <button
            type="button"
            class="absolute inset-0 bg-black/60 backdrop-blur-sm w-full h-full cursor-default"
            on:click={close}
            on:keydown={(e) => e.key === "Escape" && close()}
        ></button>

        <!-- Main Window -->
        <div
            class="relative w-full max-w-5xl h-[85vh] bg-fd-background rounded-[2.5rem] shadow-2xl flex flex-col md:flex-row overflow-hidden border border-fd-border/50 pointer-events-auto"
            in:scale={{ start: 0.95, duration: 300, opacity: 0 }}
        >
            <!-- Close Button -->
            <button
                on:click={close}
                aria-label="Đóng cửa sổ"
                class="absolute top-6 right-6 z-20 w-10 h-10 bg-fd-secondary rounded-full flex items-center justify-center text-fd-muted hover:bg-fd-destructive hover:text-white transition-all shadow-lg"
            >
                <i class="bx bx-x text-2xl"></i>
            </button>

            <!-- Left Panel: Navigation/Sub-parts -->
            <div
                class="w-full md:w-1/3 bg-fd-secondary/30 border-r border-fd-border/30 p-8 flex flex-col"
            >
                <div class="mb-8">
                    <span
                        class="text-[10px] font-black uppercase tracking-widest text-fd-primary opacity-60 mb-2 block"
                        >Khu vực giải phẫu</span
                    >
                    <h2
                        class="text-3xl font-[900] text-fd-foreground tracking-tighter leading-none"
                    >
                        {part.name}
                    </h2>
                </div>

                <div
                    class="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar"
                >
                    <p
                        class="text-sm text-fd-muted font-medium leading-relaxed mb-6"
                    >
                        {part.description}
                    </p>

                    <div class="h-px w-full bg-fd-border/30 mb-6"></div>

                    <h3
                        class="text-xs font-bold text-fd-foreground uppercase tracking-wider mb-4 flex items-center gap-2"
                    >
                        <i class="bx bx-layer text-fd-primary"></i>
                        Cấu trúc chi tiết
                    </h3>

                    <div class="space-y-3">
                        {#each part.subParts as sub}
                            <button
                                on:click={() => selectSubPart(sub)}
                                class="w-full text-left p-4 rounded-xl border transition-all duration-300 group relative overflow-hidden {selectedSubPart?.id ===
                                sub.id
                                    ? 'bg-fd-primary text-white border-fd-primary shadow-lg shadow-fd-primary/30'
                                    : 'bg-fd-card border-fd-border/40 hover:border-fd-primary/50 hover:bg-fd-card/80'}"
                            >
                                <div
                                    class="relative z-10 flex justify-between items-center"
                                >
                                    <span
                                        class="font-bold text-sm tracking-wide"
                                        >{sub.name}</span
                                    >
                                    <i
                                        class="bx bx-chevron-right text-lg opacity-50 group-hover:translate-x-1 transition-transform"
                                    ></i>
                                </div>
                            </button>
                        {/each}
                    </div>
                </div>
            </div>

            <!-- Right Panel: Detail View -->
            <div
                class="flex-1 bg-fd-background p-8 md:p-12 relative overflow-y-auto"
            >
                {#if selectedSubPart}
                    <div
                        in:fly={{ x: 20, duration: 400 }}
                        key={selectedSubPart.id}
                        class="h-full flex flex-col justify-center"
                    >
                        <div
                            class="bg-fd-primary/5 w-20 h-20 rounded-3xl flex items-center justify-center mb-8 text-fd-primary border border-fd-primary/20"
                        >
                            <i class="bx bx-dna text-4xl"></i>
                        </div>

                        <h2
                            class="text-4xl md:text-5xl font-[900] bg-clip-text text-transparent bg-gradient-to-r from-fd-foreground to-fd-muted mb-6 tracking-tighter"
                        >
                            {selectedSubPart.name}
                        </h2>

                        <div class="prose prose-lg prose-slate max-w-none">
                            <p
                                class="text-xl text-fd-foreground font-medium leading-loose mb-6"
                            >
                                {selectedSubPart.description}
                            </p>
                            {#if selectedSubPart.details}
                                <div
                                    class="bg-fd-secondary/30 p-6 rounded-2xl border-l-4 border-fd-primary"
                                >
                                    <h4
                                        class="text-sm font-black uppercase tracking-widest text-fd-primary mb-2"
                                    >
                                        Thông tin chuyên sâu
                                    </h4>
                                    <p
                                        class="text-fd-muted-foreground text-base leading-relaxed"
                                    >
                                        {selectedSubPart.details}
                                    </p>
                                </div>
                            {/if}
                        </div>
                    </div>
                {:else}
                    <div
                        class="h-full flex flex-col items-center justify-center text-center opacity-30 select-none"
                    >
                        <i class="bx bx-scan text-9xl mb-6 animate-pulse"></i>
                        <h3 class="text-2xl font-bold">
                            Chọn một bộ phận để phân tích
                        </h3>
                        <p class="text-sm font-medium mt-2">
                            Dữ liệu chi tiết sẽ hiển thị tại đây
                        </p>
                    </div>
                {/if}

                <!-- Background Decorative Grid -->
                <div
                    class="absolute inset-0 pointer-events-none opacity-[0.03]"
                    style="background-image: radial-gradient(#000 1px, transparent 1px); background-size: 20px 20px;"
                ></div>
            </div>
        </div>
    </div>
{/if}

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: transparent;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
</style>
