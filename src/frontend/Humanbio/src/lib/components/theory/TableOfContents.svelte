<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";

    let headings = $state([]);
    let activeId = $state("");

    function updateHeadings() {
        // Find all h2 and h3 elements within the prose content
        const elements = document.querySelectorAll(".prose h2, .prose h3");
        headings = Array.from(elements).map((el) => ({
            id: el.id,
            text: el.innerText,
            level: Number(el.tagName.substring(1)),
        }));
    }

    // Scroll spy implementation
    function onScroll() {
        const scrollPosition = window.scrollY + 100; // Offset for sticky header

        for (const heading of headings) {
            const element = document.getElementById(heading.id);
            if (element && element.offsetTop <= scrollPosition) {
                activeId = heading.id;
            }
        }
    }

    $effect(() => {
        // Re-run when page changes
        const _ = $page.url.pathname;
        // Small delay to ensure content is rendered
        setTimeout(() => {
            updateHeadings();
            onScroll();
        }, 100);
    });

    onMount(() => {
        updateHeadings();
        window.addEventListener("scroll", onScroll);
        return () => window.removeEventListener("scroll", onScroll);
    });

    function scrollTo(id) {
        const element = document.getElementById(id);
        if (element) {
            // Smooth scroll with offset for header
            const y = element.getBoundingClientRect().top + window.scrollY - 80;
            window.scrollTo({ top: y, behavior: "smooth" });
        }
    }
</script>

<div class="flex flex-col gap-3 relative">
    <span class="fd-label ml-0 mb-4">On this page</span>

    <!-- Main container for the "graph" -->
    <nav class="relative flex flex-col pl-4">
        <!-- The main vertical line -->
        <div class="absolute left-[7px] top-0 bottom-0 w-px bg-fd-border"></div>

        {#each headings as heading}
            <div class="relative group">
                <!-- Connector line for child items (h3) -->
                {#if heading.level === 3}
                    <div
                        class="absolute left-[-13px] top-[14px] w-[12px] h-px bg-fd-border group-hover:bg-fd-muted/30 transition-colors"
                    ></div>
                {/if}

                <button
                    onclick={() => scrollTo(heading.id)}
                    class="text-left py-1.5 pr-3 transition-all relative flex items-center gap-2 w-full rounded-md px-2 group
                    {heading.level === 3 ? 'ml-4 text-[12px]' : 'text-[13px]'}
                    {activeId === heading.id
                        ? 'text-fd-primary font-bold'
                        : 'text-fd-muted hover:text-fd-foreground hover:bg-fd-accent/50'}"
                >
                    {#if activeId === heading.id}
                        <!-- Minimal active indicator on the vertical line -->
                        <div
                            class="absolute left-[-9px] top-1.5 bottom-1.5 w-[3px] bg-fd-primary rounded-full shadow-[0_0_8px_var(--primary-glow)]"
                        ></div>
                    {/if}

                    <i
                        class="bx {heading.level === 3
                            ? 'bx-chevron-right'
                            : 'bx-hash'} {activeId === heading.id
                            ? 'opacity-100 scale-110'
                            : 'opacity-40'} transition-all"
                    ></i>

                    <div class="truncate">
                        {heading.text}
                    </div>
                </button>
            </div>
        {/each}
    </nav>
</div>
