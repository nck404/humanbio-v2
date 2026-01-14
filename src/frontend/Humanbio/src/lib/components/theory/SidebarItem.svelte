<script>
    import { slide } from "svelte/transition";
    import SidebarItem from "./SidebarItem.svelte";
    import { page } from "$app/stores";

    let { item, depth = 0 } = $props();
    let isOpen = $state(true); // Default open for now, can make smart later

    // Check if this item is active
    let isActive = $derived($page.url.pathname === `/theory/${item.slug}`);

    function toggle() {
        if (item.isFolder) {
            isOpen = !isOpen;
        }
    }
</script>

<div class="relative">
    {#if item.isFolder}
        <button
            onclick={toggle}
            class="flex items-center gap-2.5 w-full py-2 px-3 text-[13px] text-fd-muted hover:text-fd-foreground hover:bg-fd-accent/40 rounded-lg transition-all group text-left select-none mb-0.5"
        >
            <i
                class="bx bxs-folder{isOpen
                    ? '-open'
                    : ''} text-fd-primary/60 group-hover:text-fd-primary transition-colors text-base"
            ></i>
            <span class="font-bold tracking-tight">{item.name}</span>
            <i
                class="bx bx-chevron-right ml-auto text-xs transition-transform {isOpen
                    ? 'rotate-90'
                    : ''}"
            ></i>
        </button>

        {#if isOpen}
            <div
                transition:slide|local={{ duration: 250 }}
                class="relative pl-3 ml-4 border-l border-fd-border/50 space-y-0.5 mt-0.5 mb-2"
            >
                {#each item.children as child}
                    <SidebarItem item={child} depth={depth + 1} />
                {/each}
            </div>
        {/if}
    {:else}
        <a
            href={`/theory/${item.slug}`}
            class="flex items-center gap-2.5 w-full py-2 px-3 text-[13px] transition-all rounded-lg group relative overflow-hidden
            {isActive
                ? 'bg-fd-primary/8 text-fd-primary font-bold'
                : 'text-fd-muted hover:text-fd-foreground hover:bg-fd-accent'}"
        >
            {#if isActive}
                <div
                    class="absolute left-0 top-1 bottom-1 w-0.5 bg-fd-primary rounded-full"
                ></div>
            {/if}
            <i
                class="bx {isActive
                    ? 'bxs-file-blank'
                    : 'bx-file-blank'} text-base transition-transform group-hover:scale-110 {isActive
                    ? 'text-fd-primary'
                    : 'text-fd-muted group-hover:text-fd-foreground'}"
            ></i>
            <span class="truncate">{item.title}</span>

            {#if !isActive}
                <i
                    class="bx bx-chevron-right ml-auto text-xs opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all"
                ></i>
            {:else}
                <i class="bx bx-check-circle ml-auto text-sm text-fd-primary/60"
                ></i>
            {/if}
        </a>
    {/if}
</div>
