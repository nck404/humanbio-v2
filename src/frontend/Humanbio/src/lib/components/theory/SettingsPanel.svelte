<script>
    import { fade, scale } from "svelte/transition";

    let {
        fontSize = $bindable(16),
        fontFamily = $bindable("sans"),
        theme = $bindable("dark"),
        isOpen = $bindable(false),
    } = $props();

    function toggleTheme() {
        theme = theme === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", theme);
    }

    function close() {
        isOpen = false;
    }
</script>

{#if isOpen}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div
            transition:fade={{ duration: 200 }}
            class="absolute inset-0 bg-black/40 backdrop-blur-sm"
            onclick={close}
        ></div>

        <!-- Modal Window -->
        <div
            transition:scale={{ duration: 200, start: 0.95 }}
            class="relative w-full max-w-sm bg-base border border-overlay/20 rounded-xl shadow-2xl overflow-hidden p-6 gap-6 flex flex-col"
        >
            <div
                class="flex items-center justify-between pb-2 border-b border-white/5"
            >
                <h3 class="text-lg font-semibold text-text">Appearance</h3>
                <button
                    onclick={close}
                    class="text-subtle hover:text-text transition-colors"
                >
                    <i class="bx bx-x text-2xl"></i>
                </button>
            </div>

            <!-- Font Size -->
            <div class="flex flex-col gap-2">
                <div class="flex items-center justify-between">
                    <label
                        for="font-size"
                        class="text-sm font-medium text-text-muted"
                        >Font Size</label
                    >
                    <span class="text-xs text-subtle font-mono"
                        >{fontSize}px</span
                    >
                </div>
                <input
                    id="font-size"
                    type="range"
                    min="14"
                    max="22"
                    step="1"
                    bind:value={fontSize}
                    class="w-full h-2 bg-surface rounded-lg appearance-none cursor-pointer accent-iris"
                />
            </div>

            <!-- Font Family -->
            <div class="flex flex-col gap-2">
                <span class="text-sm font-medium text-text-muted"
                    >Font Family</span
                >
                <div
                    class="flex bg-surface rounded-lg p-1 border border-white/5"
                >
                    <button
                        class="flex-1 py-1.5 text-xs rounded transition-all {fontFamily ===
                        'sans'
                            ? 'bg-iris/20 text-iris font-medium'
                            : 'text-subtle hover:text-text'}"
                        onclick={() => (fontFamily = "sans")}>Sans</button
                    >
                    <button
                        class="flex-1 py-1.5 text-xs rounded transition-all {fontFamily ===
                        'serif'
                            ? 'bg-iris/20 text-iris font-medium'
                            : 'text-subtle hover:text-text'}"
                        onclick={() => (fontFamily = "serif")}>Serif</button
                    >
                    <button
                        class="flex-1 py-1.5 text-xs rounded transition-all {fontFamily ===
                        'mono'
                            ? 'bg-iris/20 text-iris font-medium'
                            : 'text-subtle hover:text-text'}"
                        onclick={() => (fontFamily = "mono")}>Mono</button
                    >
                </div>
            </div>

            <!-- Theme Toggle -->
            <div class="flex items-center justify-between pt-2">
                <span class="text-sm font-medium text-text-muted">Theme</span>
                <button
                    onclick={toggleTheme}
                    class="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 hover:border-iris/50 hover:bg-surface transition-all text-sm"
                >
                    {#if theme === "dark"}
                        <i class="bx bxs-moon text-iris"></i>
                        <span class="text-text">Dark</span>
                    {:else}
                        <i class="bx bxs-sun text-gold"></i>
                        <span class="text-text">Light</span>
                    {/if}
                </button>
            </div>
        </div>
    </div>
{/if}
