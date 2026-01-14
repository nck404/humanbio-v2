<script>
    import Sidebar from "$lib/components/theory/Sidebar.svelte";
    import ChatWidget from "$lib/components/theory/ChatWidget.svelte";
    import SearchModal from "$lib/components/theory/SearchModal.svelte";
    import TheoryNavbar from "$lib/components/theory/TheoryNavbar.svelte";
    import TableOfContents from "$lib/components/theory/TableOfContents.svelte";
    import { page } from "$app/stores";
    import { settings } from "$lib/stores/settings";
    import Highlighter from "$lib/components/theory/Highlighter.svelte";
    import { onMount, unmount } from "svelte";

    let { data, children } = $props();

    let isSearchOpen = $state(false);
    let isChatOpen = $state(false);
    let isSidebarOpen = $state(false); // Mobile sidebar toggle
    let scrollProgress = $state(0);

    function updateScrollProgress() {
        const winScroll =
            document.documentElement.scrollTop || document.body.scrollTop;
        const height =
            document.documentElement.scrollHeight -
            document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        scrollProgress = Math.min(Math.max(scrolled, 0), 100);
    }

    onMount(() => {
        window.addEventListener("scroll", updateScrollProgress);
        return () => window.removeEventListener("scroll", updateScrollProgress);
    });
</script>

<!-- Reading Progress Bar -->
<div class="fixed top-11 left-0 w-full h-0.5 z-[100] pointer-events-none">
    <div
        class="h-full bg-fd-primary transition-all duration-150 ease-out shadow-[0_0_8px_var(--primary-glow)]"
        style="width: {scrollProgress}%"
    ></div>
</div>

<SearchModal tree={data.tree} bind:isOpen={isSearchOpen} />
<ChatWidget bind:isOpen={isChatOpen} />

<div class="min-h-screen bg-fd-background text-fd-foreground flex flex-col">
    <!-- Navbar -->
    <TheoryNavbar
        onOpenSearch={() => (isSearchOpen = true)}
        onToggleSidebar={() => (isSidebarOpen = !isSidebarOpen)}
        onOpenChat={() => (isChatOpen = true)}
    />

    <div class="flex-1 max-w-[1400px] mx-auto w-full flex">
        <!-- Left Sidebar (Desktop) -->
        <aside
            class="hidden lg:block w-[260px] sticky top-[5.5rem] h-[calc(100vh-5.5rem)] overflow-y-auto border-r border-fd-border py-6 pr-4"
        >
            <Sidebar tree={data.tree} />
        </aside>

        <!-- Mobile Sidebar Drawer -->
        {#if isSidebarOpen}
            <div
                class="fixed inset-0 z-[120] lg:hidden"
                role="dialog"
                aria-modal="true"
            >
                <div
                    class="fixed inset-0 bg-black/60 backdrop-blur-md w-full h-full"
                    onclick={() => (isSidebarOpen = false)}
                    onkeydown={(e) => {
                        if (e.key === "Escape") isSidebarOpen = false;
                    }}
                    tabindex="-1"
                    aria-hidden="true"
                ></div>
                <div
                    class="fixed inset-y-0 left-0 w-[280px] bg-fd-background p-5 overflow-y-auto border-r border-fd-border shadow-2xl"
                >
                    <div class="mb-6 flex items-center gap-2">
                        <div
                            class="w-6 h-6 bg-fd-primary rounded-lg flex items-center justify-center"
                        >
                            <i class="bx bxs-component text-white text-sm"></i>
                        </div>
                        <span class="font-bold text-xs tracking-tight"
                            >HumanBio Theory</span
                        >
                    </div>
                    <Sidebar tree={data.tree} />
                </div>
            </div>
        {/if}

        <!-- Main Content -->
        <main class="flex-1 min-w-0 px-4 md:px-8 lg:px-12 py-8 lg:py-12">
            <div class="max-w-[800px] mx-auto">
                <div
                    class="prose prose-lg prose-fd max-w-none ml-0 transition-all duration-200"
                    style:font-size="{$settings.fontSize}px"
                    style:font-family={$settings.fontFamily === "sans"
                        ? "ui-sans-serif, system-ui, sans-serif"
                        : $settings.fontFamily === "serif"
                          ? "ui-serif, Georgia, serif"
                          : "ui-monospace, monospace"}
                >
                    {@render children()}
                </div>
            </div>
        </main>

        <!-- Right TOC (Desktop) -->
        <aside
            class="hidden xl:block w-[220px] sticky top-[5.5rem] h-[calc(100vh-5.5rem)] overflow-y-auto py-8 pl-4"
        >
            <TableOfContents />
        </aside>
    </div>
</div>

<style>
    /* Custom Prose adaptation for Fumadocs Theme */
    :global(.prose h1, .prose h2, .prose h3, .prose h4) {
        color: var(--foreground);
        font-weight: 800;
        letter-spacing: -0.025em;
    }
    :global(.prose strong) {
        color: var(--foreground);
        font-weight: 700;
    }
    :global(.prose blockquote) {
        border-left: 4px solid var(--secondary);
        color: #ffffff;
        font-style: italic;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        padding: 1.5rem 2rem;
        border-radius: 1rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px -5px var(--primary-glow);
        position: relative;
        overflow: hidden;
    }
    :global(.prose blockquote p) {
        color: #ffffff !important;
        margin: 0 !important;
        font-weight: 600;
        z-index: 1;
        position: relative;
    }
    :global(.prose blockquote::before) {
        content: "“";
        position: absolute;
        top: -10px;
        left: 10px;
        font-size: 5rem;
        color: rgba(255, 255, 255, 0.1);
        font-family: serif;
        pointer-events: none;
    }
    :global(.prose a) {
        color: var(--primary);
        text-decoration: underline;
        text-underline-offset: 4px;
        font-weight: 600;
    }
    :global(.prose a:hover) {
        filter: brightness(1.2);
    }
</style>
